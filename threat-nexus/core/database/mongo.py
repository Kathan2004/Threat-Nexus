from collections.abc import AsyncIterator

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from core.config.settings import get_settings


class Mongo:
    def __init__(self) -> None:
        settings = get_settings()
        self.client = AsyncIOMotorClient(settings.mongodb_uri)
        self.db = self.client[settings.mongodb_database]

    async def close(self) -> None:
        self.client.close()


mongo = Mongo()


async def get_database() -> AsyncIterator[AsyncIOMotorDatabase]:
    yield mongo.db
