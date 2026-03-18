"""Application configuration using pydantic-settings."""

import os

from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Base settings shared across all environments."""

    ENV: str
    DATABASE_URL: str


class DevSettings(AppSettings):
    """Development environment settings."""

    ENV: str = "development"
    DATABASE_URL: str = (
        "postgresql://user:password@localhost:5432/youtube_todo"
    )


class TestSettings(AppSettings):
    """Test environment settings."""

    ENV: str = "test"
    DATABASE_URL: str = (
        "postgresql://user:password@localhost:5432/youtube_todo_test"
    )


def get_settings() -> AppSettings:
    """Return settings based on the ENV environment variable."""
    env = os.getenv("ENV", "development")
    if env == "test":
        return TestSettings()
    return DevSettings()


settings = get_settings()
