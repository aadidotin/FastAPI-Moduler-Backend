from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Backend"
    APP_ENV: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = False

    # Database Setting
    DATABASE_HOST: str
    DATABASE_PORT: int = 3306
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str

    # Token Setting
    JWT_ACCESS_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    MEDIA_STORAGE_BACKEND: str = "private"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
