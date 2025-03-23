"""Settings for the Discord bot."""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the Discord bot."""

    TOKEN: str

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )


@lru_cache
def get_settings() -> Settings:
    """Get the settings for the Discord bot."""
    return Settings() #type: ignore
