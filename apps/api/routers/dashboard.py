from typing import Annotated, Any

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from core.auth.security import require_roles
from core.database.mongo import get_database
from core.models.enums import Role

router = APIRouter(tags=["dashboard"], dependencies=[Depends(require_roles(Role.ADMIN, Role.ANALYST, Role.VIEWER))])


@router.get("/dashboard")
async def dashboard(db: Annotated[AsyncIOMotorDatabase, Depends(get_database)]) -> dict[str, Any]:
    return {
        "events": await db.events.count_documents({}),
        "critical": await db.events.count_documents({"severity": "CRITICAL"}),
        "active_exploitation": await db.events.count_documents({"active_exploitation": True}),
        "alerts": await db.alerts.count_documents({}),
    }


@router.get("/analytics")
async def analytics(db: Annotated[AsyncIOMotorDatabase, Depends(get_database)]) -> dict[str, Any]:
    pipeline = [{"$group": {"_id": "$severity", "count": {"$sum": 1}}}]
    severities = {item["_id"]: item["count"] async for item in db.events.aggregate(pipeline)}
    return {"severity_distribution": severities}
