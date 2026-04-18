from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application
    ENVIRONMENT: str = "development"

    # Database
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "spa_db"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    # JWT
    JWT_ACCESS_SECRET: str = "super_secret_access_key_change_in_prod"
    JWT_REFRESH_SECRET: str = "super_secret_refresh_key_change_in_prod"
    JWT_ACCESS_EXPIRATION: int = 15  # минут
    JWT_REFRESH_EXPIRATION: int = 10080  # минут (7 дней)

    # OAuth Yandex
    YANDEX_CLIENT_ID: str = ""
    YANDEX_CLIENT_SECRET: str = ""
    YANDEX_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/oauth/yandex/callback"

    # Session
    SESSION_SECRET: str = "your_super_secret_key_here"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()