"""Centralised configuration (12-factor)."""

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # --- generic ---
    env: str = "local"                 # LOCAL / DEV / PROD
    log_level: str = "INFO"

    # --- database ---
    mongo_uri: str = "mongodb://mongo:27017/mydb"
    mongo_user: str = Field(default="", env="MONGO_USER")
    mongo_pass: str = Field(default="", env="MONGO_PASS")
    
    @property
    def mongo_connection_uri(self) -> str:
        """Build MongoDB URI with optional authentication."""
        if self.mongo_user and self.mongo_pass:
            return f"mongodb://{self.mongo_user}:{self.mongo_pass}@mongo:27017/{self.mongo_dbname}?authSource=admin"
        return self.mongo_uri
    
    @property 
    def mongo_dbname(self) -> str:
        """Get MongoDB database name."""
        return "mydb"

    # --- redis / celery ---
    redis_url: str = "redis://redis:6379/0"

    # --- security ---
    jwt_secret: str = "CHANGE_ME"

    # --- logging ---
    sentry_dsn: str | None = None
    sentry_sample_rate: float = 0.1

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local", ".env.dev", ".env.prod"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

@lru_cache  # singleton
def get_settings() -> Settings:       # used by DI & elsewhere
    return Settings()
