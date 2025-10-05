"""Application configuration managed via Pydantic settings."""

from __future__ import annotations

import functools
from typing import Any

from pydantic import AnyUrl, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.types import PostgresDsn, RedisDsn


class Settings(BaseSettings):
    """Centralized runtime configuration."""

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="allow",
        env_nested_delimiter="__",
    )

    project_name: str = "AI-Native Application Template"
    version: str = "0.1.0"
    debug: bool = True
    reload: bool = True

    backend_url: AnyUrl | None = None
    frontend_url: AnyUrl | None = None

    timezone: str = "UTC"
    default_locale: str = "en"
    supported_locales: list[str] = ["en", "es", "ru", "zh", "ar"]

    database_host: str = "postgres"
    database_port: int = 5432
    database_user: str = "app"
    database_password: str = "app"
    database_name: str = "app"
    database_dsn: str | None = None

    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str | None = None
    redis_url: str | None = None

    jwt_secret_key: str = Field(default="change-me", min_length=32)
    jwt_algorithm: str = "HS512"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 30

    sentry_dsn: str | None = None

    log_level: str = "INFO"

    security_session_token_ttl_minutes: int = 60 * 24 * 7

    allow_origins: list[str] = ["*"]
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]

    @field_validator("database_dsn", mode="before")
    @classmethod
    def assemble_db_connection(cls, value: Any, info):  # noqa: ANN001
        if value:
            return value
        data = info.data
        return str(
            PostgresDsn.build(  # type: ignore[return-value]
                scheme="postgresql+asyncpg",
                username=data.get("database_user", "app"),
                password=data.get("database_password", "app"),
                host=data.get("database_host", "postgres"),
                port=str(data.get("database_port", 5432)),
                path=f"/{data.get('database_name', 'app')}",
            )
        )

    @field_validator("redis_url", mode="before")
    @classmethod
    def assemble_redis_url(cls, value: Any, info):  # noqa: ANN001
        if value:
            return value
        data = info.data
        password = data.get("redis_password")
        auth = f":{password}@" if password else ""
        return str(
            RedisDsn(
                f"redis://{auth}{data.get('redis_host', 'redis')}:{data.get('redis_port', 6379)}/{data.get('redis_db', 0)}"
            )
        )

    async def setup(self) -> None:
        """Hook executed on app startup."""
        from app.db.session import init_engine
        from app.tasks.registry import task_registry

        await init_engine(str(self.database_dsn))
        await task_registry.setup(self)

    async def shutdown(self) -> None:
        """Hook executed on app shutdown."""
        from app.db.session import close_engine
        from app.tasks.registry import task_registry

        await task_registry.shutdown()
        await close_engine()


@functools.lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
