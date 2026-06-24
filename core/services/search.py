from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase


class SearchService:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db = db

    async def search(self, query: str, collections: list[str], limit: int = 25) -> list[dict[str, Any]]:
        if not query.strip():
            return []
        results: list[dict[str, Any]] = []
        for collection_name in collections:
            cursor = self.db[collection_name].find(
                {"$text": {"$search": query}},
                {"_id": 0, "score": {"$meta": "textScore"}},
            ).sort([("score", {"$meta": "textScore"})]).limit(limit)
            async for item in cursor:
                item["collection"] = collection_name
                results.append(item)
        return sorted(results, key=lambda item: item.get("score", 0), reverse=True)[:limit]
