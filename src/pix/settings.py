from typing import Literal

from pydantic import SecretStr, ValidationError
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)
from rich.console import Console


class Settings(BaseSettings):
    token: SecretStr
    log_level: Literal["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]

    model_config = SettingsConfigDict(
        frozen=True,
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="PIX_",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return init_settings, env_settings, dotenv_settings


def load_settings() -> Settings:
    try:
        return Settings()  # pyright: ignore[reportCallIssue] https://github.com/pydantic/pydantic-settings/issues/201
    except ValidationError as e:
        _display_errors(e)
        raise SystemExit(1) from e


def _format_loc(loc: tuple[str | int, ...]) -> str:
    path = ""

    for idx, segment in enumerate(loc):
        match segment:
            case str():
                if idx > 0:
                    path += "."
                path += segment
            case int():
                path += f"[{segment}]"

    return path


def _display_errors(error: ValidationError) -> None:
    console = Console(stderr=True, highlight=False)
    count = error.error_count()
    plural = "s" if count > 1 else ""

    console.print(f"[red]Failed to validate settings ({count} error{plural}):[/]")

    for err in error.errors():
        msg = err["msg"]
        value = repr(err["input"])
        loc = _format_loc(err["loc"])

        console.print(f"* [bold]{loc}[/]: {msg} - got [italic red]{value}[/].")

    console.print("\n[dim]Tip: Check your .env file or environment variables.[/]")
