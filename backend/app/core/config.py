from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App
    APP_NAME: str = "JobFinder"
    APP_VERSION: str = "1.0.0"
    APP_DEBUG: bool = True
    APP_ENV: str = "development"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://localhost:5432/jobfinder"
    DATABASE_URL_SYNC: str = "postgresql://localhost:5432/jobfinder"

    # Security (future)
    SECRET_KEY: str = "super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Scrapers
    REMOTIVE_BASE_URL: str = "https://remotive.com/api"
    FINDWORK_API_KEY: str = ""
    FINDWORK_BASE_URL: str = "https://findwork.dev/api"
    ADZUNA_APP_ID: str = ""
    ADZUNA_API_KEY: str = ""
    ADZUNA_BASE_URL: str = "https://api.adzuna.com/v1/api"

    # Scheduler
    SYNC_INTERVAL_HOURS: int = 6

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    # Logging
    LOG_LEVEL: str = "INFO"


settings = Settings()
