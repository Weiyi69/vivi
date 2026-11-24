import os

import pytest
from pydantic import ValidationError

os.environ.setdefault("PUBLIC_APP_URL", "http://localhost:3000")
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:test@127.0.0.1:5432/vivi",
)
os.environ.setdefault(
    "SESSION_SECRET",
    "test-secret-that-is-at-least-32-characters",
)

from app.core.config import Settings, get_settings


def test_settings_load():
    settings = get_settings()
    assert settings.app_name == "Vivi"
    assert settings.cors_origins == ["http://localhost:3000"]


def test_database_url_validation():
    with pytest.raises(ValidationError):
        Settings(
            public_app_url="http://localhost:3000",
            database_url="sqlite:///test.db",
            session_secret="test-secret-that-is-at-least-32-characters",
        )
