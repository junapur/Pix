import logging

import hikari
import lightbulb
from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install

import pix.extensions
from pix.settings import Settings, load_settings

logger = logging.getLogger(__name__)


def main() -> None:
    install()
    settings = load_settings()

    logging.basicConfig(
        level=settings.log_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=Console(stderr=True), rich_tracebacks=True)],
    )

    bot = hikari.GatewayBot(token=settings.token.get_secret_value())
    client = lightbulb.client_from_app(bot)

    @bot.listen(hikari.StartingEvent)
    async def on_starting(_: hikari.StartingEvent) -> None:  # pyright: ignore[reportUnusedFunction]
        registry = client.di.registry_for(lightbulb.di.Contexts.DEFAULT)
        registry.register_value(Settings, settings)

        await client.load_extensions_from_package(pix.extensions)
        await client.start()

    try:
        bot.run()
    except hikari.UnauthorizedError:
        logger.critical(
            "Failed to authenticate with Discord. Ensure your bot token is valid."
        )
