from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from core.auth.security import require_roles
from core.database.mongo import get_database
from core.models.enums import Role
from core.services.search import SearchService

router = APIRouter(prefix="/search", tags=["search"], dependencies=[Depends(require_roles(Role.ADMIN, Role.ANALYST, Role.VIEWER))])


@router.get("")
async def search(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_database)],
    q: str = Query(min_length=2),
    limit: int = Query(25, ge=1, le=100),
) -> list[dict[str, Any]]:
    collections = ["events", "cves", "actors", "campaigns", "malware", "iocs"]
    return await SearchService(db).search(q, collections, limit)
