from __future__ import annotations

from functools import lru_cache
from typing import Any, List

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env", "../../.env"),
        env_file_encoding="utf-8",
        extra="allow",
    )

    app_name: str = "AI Ready Backend"
    app_env: str = Field(default="development", validation_alias="APP_ENV")
    debug: bool = Field(default=False, validation_alias="DEBUG")
    secret_key: str = Field(default="change-me", validation_alias="SECRET_KEY")

    api_v1_prefix: str = "/api/v1"
    docs_url: str | None = Field(default="/docs")
    openapi_url: str = "/openapi.json"

    database_url: str = Field(default="postgresql+asyncpg://postgres:postgres@db:5432/app")
    sync_database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@db:5432/app",
        validation_alias="SYNC_DATABASE_URL",
    )

    redis_url: str = Field(default="redis://redis:6379/0")

    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7
    pre_auth_token_expire_minutes: int = 60 * 24

    cors_allow_origins: List[AnyHttpUrl] = Field(default_factory=list)
    cors_allow_credentials: bool = True

    sentry_dsn: str | None = None
    log_level: str = "INFO"

    default_locale: str = "en"
    supported_locales: List[str] = Field(default_factory=lambda: ["en", "ru", "es", "zh", "ar"])

    timezone: str = Field(default="UTC")

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[arg-type]


settings = get_settings()
