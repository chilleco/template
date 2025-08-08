from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My FinApp"
    debug: bool = False
    database_url: str
    secret_key: str
    redis_url: str
    # другие настройки: URLs внешних API, ключи интеграций, etc.
    class Config:
        env_file = ".env"

settings = Settings()
