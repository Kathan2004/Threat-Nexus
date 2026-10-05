from motor.motor_asyncio import AsyncIOMotorDatabase

from core.models.domain import CVE, IOC, Alert, Campaign, Malware, ThreatActor, ThreatEvent
from core.models.graph import Relationship
from core.repositories.base import MongoRepository


class EventRepository(MongoRepository[ThreatEvent]):
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        super().__init__(db, "events", ThreatEvent)

    async def ensure_indexes(self) -> None:
        await super().ensure_indexes()
        await self.collection.create_index([("title", "text"), ("description", "text")])
        await self.collection.create_index("severity")
        await self.collection.create_index("confidence")


class IOCRepository(MongoRepository[IOC]):
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        super().__init__(db, "iocs", IOC)

    async def ensure_indexes(self) -> None:
        await super().ensure_indexes()
        await self.collection.create_index([("type", 1), ("value", 1)], unique=True)


class CVERepository(MongoRepository[CVE]):
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        super().__init__(db, "cves", CVE)

    async def ensure_indexes(self) -> None:
        await super().ensure_indexes()
        await self.collection.create_index("cve_id", unique=True)


class ActorRepository(MongoRepository[ThreatActor]):
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        super().__init__(db, "actors", ThreatActor)


class CampaignRepository(MongoRepository[Campaign]):
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        super().__init__(db, "campaigns", Campaign)


class MalwareRepository(MongoRepository[Malware]):
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        super().__init__(db, "malware", Malware)


class AlertRepository(MongoRepository[Alert]):
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        super().__init__(db, "alerts", Alert)


class RelationshipRepository(MongoRepository[Relationship]):
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        super().__init__(db, "relationships", Relationship)
