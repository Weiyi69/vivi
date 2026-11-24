from functools import lru_cache
from typing import Literal

from pydantic import Field, HttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    app_name: str = "Vivi"
    app_env: Literal["development", "test", "production"] = "development"
    public_app_url: HttpUrl
    database_url: str
    session_secret: str = Field(min_length=32)
    secure_cookies: bool = False
    log_level: str = "INFO"
    cors_origins: list[str] = ["http://localhost:3000"]
    trusted_origins: list[str] = ["http://localhost:3000"]

    @field_validator("cors_origins", "trusted_origins", mode="before")
    @classmethod
    def split_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, value: str) -> str:
        if not value.startswith("postgresql+psycopg://"):
            raise ValueError("DATABASE_URL must use the postgresql+psycopg scheme")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
