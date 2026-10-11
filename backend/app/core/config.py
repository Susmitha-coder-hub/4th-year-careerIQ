"""
backend/app/core/config.py
Configuration settings for CareerFit backend.
"""

import os
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "CareerFit API"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "careerfit.db")
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "5"))
    CORS_ORIGINS: list = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]

settings = Settings()
