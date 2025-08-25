# app/config.py

from __future__ import annotations
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

# Load .env from the backend folder
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # .../backend
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

class Settings(BaseModel):
    # Indent everything inside the class (4 spaces)
    database_url: str = os.getenv("DATABASE_URL") or ""
    redis_url: str = os.getenv("REDIS_URL") or "redis://localhost:6379/0"

    keepa_api_key: str = os.getenv("KEEPA_API_KEY") or ""
    paapi_access_key: str = os.getenv("PAAPI_ACCESS_KEY") or ""
    paapi_secret_key: str = os.getenv("PAAPI_SECRET_KEY") or ""
    paapi_associate_tag: str = os.getenv("PAAPI_ASSOCIATE_TAG") or ""
    paapi_region: str = os.getenv("PAAPI_REGION") or "us-east-1"

    allowed_origins: List[str] = (
        os.getenv("ALLOWED_ORIGINS") or "http://localhost:3000"
    ).split(",")

settings = Settings()
