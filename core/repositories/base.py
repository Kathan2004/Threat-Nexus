from typing import Any, Generic, TypeVar

from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel

ModelT = TypeVar("ModelT", bound=BaseModel)


class MongoRepository(Generic[ModelT]):
    def __init__(self, db: AsyncIOMotorDatabase, collection: str, model: type[ModelT]) -> None:
        self.collection = db[collection]
        self.model = model

    async def ensure_indexes(self) -> None:
        await self.collection.create_index("id", unique=True)
        await self.collection.create_index("created_at")

    async def upsert(self, item: ModelT) -> ModelT:
        payload = item.model_dump(mode="json")
        await self.collection.update_one({"id": payload["id"]}, {"$set": payload}, upsert=True)
        return item

    async def get(self, entity_id: str) -> ModelT | None:
        data = await self.collection.find_one({"id": entity_id}, {"_id": 0})
        return self.model.model_validate(data) if data else None

    async def find_one(self, query: dict[str, Any]) -> ModelT | None:
        data = await self.collection.find_one(query, {"_id": 0})
        return self.model.model_validate(data) if data else None

    async def list(
        self,
        query: dict[str, Any] | None = None,
        limit: int = 50,
        offset: int = 0,
        sort: str = "-created_at",
    ) -> tuple[list[ModelT], int]:
        query = query or {}
        direction = -1 if sort.startswith("-") else 1
        sort_field = sort.lstrip("-")
        cursor = self.collection.find(query, {"_id": 0}).sort(sort_field, direction).skip(offset).limit(limit)
        total = await self.collection.count_documents(query)
        return [self.model.model_validate(doc) async for doc in cursor], total
