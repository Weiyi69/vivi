import os
from pathlib import Path

import pytest

os.environ["APP_ENV"] = "test"
os.environ["PUBLIC_APP_URL"] = "http://localhost:3000/"
os.environ["DATABASE_URL"] = (
    "postgresql+psycopg://postgres:ViviPhase1Local!@127.0.0.1:5432/vivi_test"
)
os.environ["SESSION_SECRET"] = "test-secret-that-is-at-least-32-characters"
os.environ["EMAIL_MODE"] = "development"
os.environ["DEVELOPMENT_OUTBOX_DIR"] = str(Path(__file__).parent / ".test-outbox")
os.environ["CORS_ORIGINS"] = '["http://localhost:3000"]'
os.environ["TRUSTED_ORIGINS"] = '["http://localhost:3000"]'

from app.core.database import SessionLocal
from app.models.auth import (
    AuthenticationRateLimit,
    PasswordResetToken,
    User,
    UserSession,
    VerificationToken,
)


@pytest.fixture(autouse=True)
def clean_auth_tables():
    db = SessionLocal()
    try:
        outbox = Path(__file__).parent / ".test-outbox"
        if outbox.exists():
            for file in outbox.glob("*.txt"):
                file.unlink()
        db.query(AuthenticationRateLimit).delete()
        db.query(UserSession).delete()
        db.query(PasswordResetToken).delete()
        db.query(VerificationToken).delete()
        db.query(User).delete()
        db.commit()
        yield db
    finally:
        db.close()
