"""Settings for the Discord bot."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


@lru_cache
class Settings(BaseSettings):
    """Settings for the Discord bot."""

    DISCORD_BOT_TOKEN: str
    API_URL: str

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )


@lru_cache
def get_settings() -> Settings:
    """Get the settings for the Discord bot."""
    return Settings() # type: ignore[call-arg]
