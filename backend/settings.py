import os
from functools import lru_cache
from typing import List, Optional

from dotenv import load_dotenv, find_dotenv

# Load .env from the project root and override anything stale in the shell
load_dotenv(find_dotenv(), override=True)


class Settings:
    # App / CORS
    app_name: str = "Business Licensing Assistant"
    allow_origins: List[str] = ["http://localhost", "http://127.0.0.1", "*"]

    # Data path
    data_path: str = os.getenv("RULES_PATH", "backend/data/rules.json")

    # === Gemini / Google ===
    google_api_key: Optional[str] = os.getenv("GOOGLE_API_KEY")
    # Good defaults: "gemini-1.5-flash" (fast, cheap) or "gemini-1.5-pro" (higher quality)
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")


@lru_cache
def get_settings() -> Settings:
    """
    Import and call get_settings() anywhere:
      from backend.settings import get_settings
      settings = get_settings()
    """
    return Settings()
