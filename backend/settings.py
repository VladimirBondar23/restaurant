from pydantic import BaseModel
from functools import lru_cache
import os

class Settings(BaseModel):
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    data_path: str = os.getenv("RULES_PATH", "backend/data/rules.json")
    app_name: str = "Business Licensing Assistant"
    allow_origins: list[str] = ["http://localhost", "http://127.0.0.1", "*"]

@lru_cache
def get_settings() -> Settings:
    return Settings()
