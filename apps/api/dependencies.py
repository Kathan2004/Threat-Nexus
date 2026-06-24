from collections.abc import AsyncIterator

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from core.database.mongo import get_database
from core.repositories.intel import (
    ActorRepository,
    AlertRepository,
    CVERepository,
    CampaignRepository,
    EventRepository,
    IOCRepository,
    MalwareRepository,
    RelationshipRepository,
)


async def event_repo(db: AsyncIOMotorDatabase = Depends(get_database)) -> AsyncIterator[EventRepository]:
    yield EventRepository(db)


async def alert_repo(db: AsyncIOMotorDatabase = Depends(get_database)) -> AsyncIterator[AlertRepository]:
    yield AlertRepository(db)


async def cve_repo(db: AsyncIOMotorDatabase = Depends(get_database)) -> AsyncIterator[CVERepository]:
    yield CVERepository(db)


async def ioc_repo(db: AsyncIOMotorDatabase = Depends(get_database)) -> AsyncIterator[IOCRepository]:
    yield IOCRepository(db)


async def actor_repo(db: AsyncIOMotorDatabase = Depends(get_database)) -> AsyncIterator[ActorRepository]:
    yield ActorRepository(db)


async def campaign_repo(db: AsyncIOMotorDatabase = Depends(get_database)) -> AsyncIterator[CampaignRepository]:
    yield CampaignRepository(db)


async def malware_repo(db: AsyncIOMotorDatabase = Depends(get_database)) -> AsyncIterator[MalwareRepository]:
    yield MalwareRepository(db)


async def relationship_repo(db: AsyncIOMotorDatabase = Depends(get_database)) -> AsyncIterator[RelationshipRepository]:
    yield RelationshipRepository(db)
