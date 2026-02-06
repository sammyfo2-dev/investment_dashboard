from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://investing_user:dev_password@localhost:5432/investing_tool"
    REDIS_URL: str = "redis://localhost:6379"

    # Optional: Claude API
    ANTHROPIC_API_KEY: str = ""

    # Application
    SECRET_KEY: str = "change-this-in-production"
    DEBUG: bool = True

    # Background Tasks
    DAILY_UPDATE_HOUR: int = 6
    TIMEZONE: str = "America/New_York"

    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 10
    UPLOAD_DIR: str = "./uploads"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
