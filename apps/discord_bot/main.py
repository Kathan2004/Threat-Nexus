import discord
import structlog

from core.config.settings import get_settings
from core.logging.config import configure_logging

logger = structlog.get_logger()


def build_client() -> discord.Client:
    intents = discord.Intents.default()
    intents.guilds = True
    intents.messages = True
    return discord.Client(intents=intents)


def main() -> None:
    configure_logging()
    settings = get_settings()
    if not settings.discord_token:
        raise RuntimeError("DISCORD_TOKEN is required")
    client = build_client()

    @client.event
    async def on_ready() -> None:
        logger.info("discord_ready", user=str(client.user))

    client.run(settings.discord_token)


if __name__ == "__main__":
    main()
