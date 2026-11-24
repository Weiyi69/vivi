from datetime import UTC, datetime

from fastapi import HTTPException, Request, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.models.auth import AuthenticationRateLimit


def _ip_key(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
    if forwarded:
        return forwarded
    if request.client:
        return request.client.host
    return "unknown"


def enforce_rate_limit(
    db: Session,
    settings: Settings,
    request: Request,
    action: str,
    limit: int,
) -> None:
    key = f"{action}:{_ip_key(request)}"
    now = datetime.now(UTC)
    try:
        row = (
            db.query(AuthenticationRateLimit)
            .filter(AuthenticationRateLimit.key == key)
            .one_or_none()
        )
        if row is None:
            row = AuthenticationRateLimit(
                key=key,
                window_started_at=now,
                count=1,
            )
            db.add(row)
            db.commit()
            return
        elapsed = (now - row.window_started_at).total_seconds()
        if elapsed >= settings.rate_limit_window_seconds:
            row.window_started_at = now
            row.count = 1
            db.commit()
            return
        if row.count >= limit:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests",
            )
        row.count += 1
        db.commit()
    except IntegrityError:
        db.rollback()
        enforce_rate_limit(db, settings, request, action, limit)
