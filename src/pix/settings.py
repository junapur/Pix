from typing import Literal

from pydantic import SecretStr, ValidationError
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)
from rich.console import Console
from rich.tree import Tree


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


def _display_errors(error: ValidationError) -> None:
    console = Console(stderr=True)
    count = error.error_count()
    plural = "s" if count > 1 else ""

    tree = Tree(f"[red]Failed to validate settings ({count} error{plural})[/]")

    for err in error.errors():
        msg = err["msg"]
        value = repr(err["input"])
        field = ".".join(str(loc) for loc in err["loc"])

        tree.add(f"[bold]{field}[/]: {msg} - got [italic red]{value}[/]")

    console.print(tree)
    console.print("\n[dim]Tip: Check your .env file or environment variables.[/]")
