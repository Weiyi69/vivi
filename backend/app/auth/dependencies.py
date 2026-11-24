from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import challenge_hash, utcnow
from app.models.auth import User, UserSession


def get_current_user(
    vivi_session: str | None = Cookie(default=None, alias="VIVI_SESSION"),
    db: Session = Depends(get_db),
) -> User:
    if not vivi_session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )
    session = (
        db.query(UserSession)
        .filter(
            UserSession.token_hash == challenge_hash(vivi_session),
            UserSession.revoked_at.is_(None),
        )
        .one_or_none()
    )
    now = utcnow()
    if session is None or session.expires_at <= now:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )
    user = db.get(User, session.user_id)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )
    if user.email_verified_at is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Email verification required"
        )
    session.last_used_at = now
    db.commit()
    return user
