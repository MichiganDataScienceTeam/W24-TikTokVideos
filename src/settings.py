from typing import Any

from pydantic import HttpUrl, PositiveInt, PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseSettings):
    """Settings for this API.

    Modified from: https://stackoverflow.com/a/77506150
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="allow"
    )

    REDDIT_CLIENT_APP_ID: str
    REDDIT_CLIENT_SECRET: str
    REDDIT_CLIENT_ACC_NAME: str

    PICO_VOICE_API_KEY: str

settings = APISettings()