from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from core.auth.security import Principal, get_principal, require_roles
from core.database.mongo import get_database
from core.models.enums import Role
from core.models.source_config import SourceConfigUpdate, SourceConfigView
from core.services.source_config import SourceConfigService

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get(
    "/sources", response_model=list[SourceConfigView], dependencies=[Depends(require_roles(Role.ADMIN, Role.ANALYST))]
)
async def list_sources(db: Annotated[AsyncIOMotorDatabase, Depends(get_database)]) -> list[SourceConfigView]:
    return await SourceConfigService(db).list_sources()


@router.put("/sources/{source_id}", response_model=SourceConfigView, dependencies=[Depends(require_roles(Role.ADMIN))])
async def update_source(
    source_id: str,
    update: SourceConfigUpdate,
    db: Annotated[AsyncIOMotorDatabase, Depends(get_database)],
    principal: Annotated[Principal, Depends(get_principal)],
) -> SourceConfigView:
    try:
        return await SourceConfigService(db).update_source(source_id, update, principal.subject)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Unknown source") from exc
