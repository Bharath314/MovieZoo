from typing import Annotated, Literal

from pydantic import AnyUrl, EmailStr, HttpUrl, UrlConstraints
from pydantic_settings import BaseSettings, SettingsConfigDict

SQLiteDsn = Annotated[
    AnyUrl, UrlConstraints(allowed_schemes=["sqlite", "sqlite+aiosqlite"])
]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    FRONTEND_HOST: str = "http://localhost:5173"
    FASTAPI_ENV: Literal["development"] | None = "development"

    PROJECT_NAME: str = "MovieZoo API"
    SENTRY_DSN: HttpUrl | None = None
    DATABASE_URL: SQLiteDsn = "sqlite:///database.db"
    FIRST_SUPERUSER: EmailStr = "abc@xyz.com"
    FIRST_SUPERUSER_PASSWORD: str = "12345678"


settings = Settings()
