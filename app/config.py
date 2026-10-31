from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Literal

class Settings(BaseSettings):
    database_url: str
    test_db: str | None = None

    log_level: str = "INFO"
    http_log_level: str = "WARNING"

    secret_key: str = Field(min_length=32)
    
    algorithm: Literal["HS256"]
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    rawg_api: str
    tmdb_token: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()