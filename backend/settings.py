import os
from functools import lru_cache
from typing import List, Optional
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

BACKEND_DIR = Path(__file__).resolve().parent
DEFAULT_RULES = BACKEND_DIR / "data" / "rules.json"

class Settings:
    # App / CORS
    app_name: str = "Business Licensing Assistant"
    allow_origins: List[str] = ["http://localhost", "http://127.0.0.1", "*"]

    # Data path (absolute)
    data_path: str = str(
        Path(os.getenv("RULES_PATH", str(DEFAULT_RULES))).resolve()
    )

    # Gemini config
    google_api_key: Optional[str] = os.getenv("GOOGLE_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

@lru_cache
def get_settings() -> Settings:
    return Settings()
