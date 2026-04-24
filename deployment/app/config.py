from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized configuration for the deployment API and graph service."""

    groq_api_key: str = Field(alias="GROQ_API_KEY")
    model_name: str = Field(default="llama-3.1-8b-instant", alias="MODEL_NAME")
    max_iterations: int = Field(default=4, alias="MAX_ITERATIONS")
    request_timeout_seconds: int = Field(default=45, alias="REQUEST_TIMEOUT_SECONDS")
    environment: str = Field(default="development", alias="ENVIRONMENT")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()