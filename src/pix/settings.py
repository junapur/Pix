from typing import Literal

from pydantic import SecretStr
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    token: SecretStr
    log_level: Literal["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]

    model_config = SettingsConfigDict(
        frozen=True,
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="PIX_",
    )
