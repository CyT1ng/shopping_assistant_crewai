from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Model provider keys (set what you use)
    openai_api_key: str | None = None

    # Tools
    serper_api_key: str | None = None
    bestbuy_api_key: str | None = None
    walmart_api_key: str | None = None

    # App defaults
    log_level: str = "INFO"
    default_currency: str = "USD"
    default_region: str = "US"


settings = Settings()
