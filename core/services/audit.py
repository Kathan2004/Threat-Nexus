from datetime import UTC, datetime
from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase


class AuditService:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.collection = db["audit_logs"]

    async def record(self, actor: str, action: str, target: str, metadata: dict[str, Any] | None = None) -> None:
        await self.collection.insert_one(
            {
                "actor": actor,
                "action": action,
                "target": target,
                "metadata": metadata or {},
                "created_at": datetime.now(UTC),
            }
        )
