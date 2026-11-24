from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.rate_limit import enforce_rate_limit
from app.auth.schemas import (
    ChallengeConfirmRequest,
    ChallengeRequest,
    ChangePasswordRequest,
    LoginRequest,
    PasswordResetRequest,
    ProfileUpdateRequest,
    RegisterRequest,
)
from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import (
    challenge_hash,
    hash_password,
    normalize_email,
    password_needs_rehash,
    random_challenge,
    utcnow,
    validate_display_name,
    validate_password,
    verify_password,
)
from app.email.delivery import EmailDeliveryError, get_email_delivery
from app.models.auth import PasswordResetToken, User, UserSession, VerificationToken

router = APIRouter(prefix="/auth", tags=["authentication"])
SESSION_COOKIE = "VIVI_SESSION"
CSRF_COOKIE = "VIVI_CSRF"


def cookie_settings() -> dict:
    settings = get_settings()
    return {
        "httponly": True,
        "secure": settings.secure_cookies,
        "samesite": "lax",
        "path": "/",
    }


def set_session(response: Response, db: Session, user: User) -> None:
    settings = get_settings()
    raw_token = random_challenge()
    expires = utcnow() + timedelta(days=settings.session_days)
    db.add(
        UserSession(
            user_id=user.id,
            token_hash=challenge_hash(raw_token),
            expires_at=expires,
        )
    )
    db.commit()
    response.set_cookie(
        SESSION_COOKIE,
        raw_token,
        max_age=settings.session_days * 24 * 60 * 60,
        **cookie_settings(),
    )


@router.get("/csrf")
async def csrf(response: Response):
    settings = get_settings()
    token = random_challenge()
    response.set_cookie(
        CSRF_COOKIE,
        token,
        httponly=False,
        secure=settings.secure_cookies,
        samesite="lax",
        path="/",
    )
    return {"csrf_token": token}


@router.post("/register", status_code=status.HTTP_202_ACCEPTED)
async def register(
    payload: RegisterRequest, request: Request, db: Session = Depends(get_db)
):
    settings = get_settings()
    enforce_rate_limit(db, settings, request, "register", 5)
    normalized = normalize_email(str(payload.email))
    if payload.password != payload.password_confirmation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match"
        )
    try:
        validate_password(payload.password)
        display_name = validate_display_name(payload.display_name)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc

    existing = db.query(User).filter(User.normalized_email == normalized).one_or_none()
    if existing is not None:
        return {
            "message": "If the email is eligible, a verification message will be sent"
        }

    user = User(
        email=str(payload.email).strip(),
        normalized_email=normalized,
        password_hash=hash_password(payload.password),
        display_name=display_name,
    )
    db.add(user)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        return {
            "message": "If the email is eligible, a verification message will be sent"
        }

    raw_token = random_challenge()
    db.query(VerificationToken).filter(
        VerificationToken.user_id == user.id,
        VerificationToken.used_at.is_(None),
    ).update({VerificationToken.used_at: utcnow()})
    challenge = VerificationToken(
        user_id=user.id,
        token_hash=challenge_hash(raw_token),
        expires_at=utcnow() + timedelta(hours=24),
    )
    db.add(challenge)

    try:
        delivery = get_email_delivery(settings)
        link = f"{settings.public_app_url}auth/verify-email?token={raw_token}"
        delivery.send(
            recipient=str(payload.email),
            subject="Verify your Vivi account",
            body=f"Use this link to verify your Vivi account:\n{link}\n",
        )
        db.commit()
    except EmailDeliveryError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Email delivery is unavailable",
        ) from exc

    return {"message": "If the email is eligible, a verification message will be sent"}


@router.post("/login")
async def login(
    payload: LoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    settings = get_settings()
    enforce_rate_limit(db, settings, request, "login", 10)
    normalized = normalize_email(str(payload.email))
    generic = "Invalid email or password"
    user = db.query(User).filter(User.normalized_email == normalized).one_or_none()
    if user is None or not verify_password(user.password_hash, payload.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=generic)
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=generic)
    if user.email_verified_at is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Email verification required"
        )
    if password_needs_rehash(user.password_hash):
        user.password_hash = hash_password(payload.password)
    user.last_login_at = utcnow()
    db.commit()
    set_session(response, db, user)
    return {"message": "Logged in"}


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    raw = request.cookies.get(SESSION_COOKIE)
    if raw:
        db.query(UserSession).filter(
            UserSession.token_hash == challenge_hash(raw)
        ).update({UserSession.revoked_at: utcnow()})
        db.commit()
    response.delete_cookie(SESSION_COOKIE, path="/")
    response.delete_cookie(CSRF_COOKIE, path="/")
    return {"message": "Logged out"}


@router.post("/verify-email")
async def verify_email(payload: ChallengeConfirmRequest, db: Session = Depends(get_db)):
    challenge = (
        db.query(VerificationToken)
        .filter(
            VerificationToken.token_hash == challenge_hash(payload.token),
            VerificationToken.used_at.is_(None),
            VerificationToken.expires_at > utcnow(),
        )
        .one_or_none()
    )
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification link is invalid or expired",
        )
    user = db.get(User, challenge.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification link is invalid or expired",
        )
    challenge.used_at = utcnow()
    user.email_verified_at = utcnow()
    db.commit()
    return {"message": "Email verified"}


@router.post("/resend-verification")
async def resend_verification(
    payload: ChallengeRequest, request: Request, db: Session = Depends(get_db)
):
    settings = get_settings()
    enforce_rate_limit(db, settings, request, "resend_verification", 3)
    normalized = normalize_email(str(payload.email))
    user = (
        db.query(User)
        .filter(
            User.normalized_email == normalized,
            User.email_verified_at.is_(None),
            User.is_active.is_(True),
        )
        .one_or_none()
    )
    if user is not None:
        try:
            delivery = get_email_delivery(settings)
            db.query(VerificationToken).filter(
                VerificationToken.user_id == user.id,
                VerificationToken.used_at.is_(None),
            ).update({VerificationToken.used_at: utcnow()})
            raw = random_challenge()
            db.add(
                VerificationToken(
                    user_id=user.id,
                    token_hash=challenge_hash(raw),
                    expires_at=utcnow() + timedelta(hours=24),
                )
            )
            link = f"{settings.public_app_url}auth/verify-email?token={raw}"
            delivery.send(
                str(payload.email),
                "Verify your Vivi account",
                f"Use this link:\n{link}\n",
            )
            db.commit()
        except EmailDeliveryError as exc:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Email delivery is unavailable",
            ) from exc
    return {
        "message": "If an eligible account exists, a verification message will be sent"
    }


@router.post("/password-reset/request")
async def request_password_reset(
    payload: ChallengeRequest, request: Request, db: Session = Depends(get_db)
):
    settings = get_settings()
    enforce_rate_limit(db, settings, request, "password_reset_request", 3)
    normalized = normalize_email(str(payload.email))
    user = (
        db.query(User)
        .filter(
            User.normalized_email == normalized,
            User.email_verified_at.is_not(None),
            User.is_active.is_(True),
        )
        .one_or_none()
    )
    if user is not None:
        try:
            delivery = get_email_delivery(settings)
            db.query(PasswordResetToken).filter(
                PasswordResetToken.user_id == user.id,
                PasswordResetToken.used_at.is_(None),
            ).update({PasswordResetToken.used_at: utcnow()})
            raw = random_challenge()
            db.add(
                PasswordResetToken(
                    user_id=user.id,
                    token_hash=challenge_hash(raw),
                    expires_at=utcnow() + timedelta(hours=1),
                )
            )
            link = f"{settings.public_app_url}auth/reset-password?token={raw}"
            delivery.send(
                str(payload.email),
                "Reset your Vivi password",
                f"Use this link:\n{link}\n",
            )
            db.commit()
        except EmailDeliveryError as exc:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Email delivery is unavailable",
            ) from exc
    return {"message": "If an eligible account exists, a reset message will be sent"}


@router.post("/password-reset/confirm")
async def confirm_password_reset(
    payload: PasswordResetRequest, db: Session = Depends(get_db)
):
    if payload.password != payload.password_confirmation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match"
        )
    try:
        validate_password(payload.password)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
    challenge = (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.token_hash == challenge_hash(payload.token),
            PasswordResetToken.used_at.is_(None),
            PasswordResetToken.expires_at > utcnow(),
        )
        .one_or_none()
    )
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset link is invalid or expired",
        )
    user = db.get(User, challenge.user_id)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset link is invalid or expired",
        )
    challenge.used_at = utcnow()
    user.password_hash = hash_password(payload.password)
    user.updated_at = utcnow()
    db.query(UserSession).filter(
        UserSession.user_id == user.id,
        UserSession.revoked_at.is_(None),
    ).update({UserSession.revoked_at: utcnow()})
    db.commit()
    return {"message": "Password reset successfully"}


@router.get("/me")
async def profile(user: User = Depends(get_current_user)):
    return {
        "id": str(user.id),
        "email": user.email,
        "display_name": user.display_name,
        "email_verified": user.email_verified_at is not None,
    }


@router.patch("/me")
async def update_profile(
    payload: ProfileUpdateRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        user.display_name = validate_display_name(payload.display_name)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
    user.updated_at = utcnow()
    db.commit()
    return {"message": "Profile updated", "display_name": user.display_name}


@router.post("/change-password")
async def change_password(
    payload: ChangePasswordRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if payload.new_password != payload.new_password_confirmation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match"
        )
    if not verify_password(user.password_hash, payload.current_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )
    try:
        validate_password(payload.new_password)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
    user.password_hash = hash_password(payload.new_password)
    user.updated_at = utcnow()
    db.query(UserSession).filter(
        UserSession.user_id == user.id,
        UserSession.revoked_at.is_(None),
    ).update({UserSession.revoked_at: utcnow()})
    db.commit()
    return {"message": "Password changed"}
