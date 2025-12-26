from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/SQG/content/v1"

    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://localhost:3000",
        "https://localhost:8000",
        "http://localhost:5173",
        "https://localhost:5173",
    ]

    PROJECT_NAME: str = "SQL Query Generator Platform APIs"

    DATABASE_URL: str
    GOOGLE_API_KEY: str

    # Optional / legacy
    gemini_api_key: str | None = None
    llm_provider: str | None = None

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
