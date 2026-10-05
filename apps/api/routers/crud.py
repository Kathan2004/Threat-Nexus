from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from apps.api.dependencies import (
    actor_repo,
    alert_repo,
    campaign_repo,
    cve_repo,
    event_repo,
    ioc_repo,
    malware_repo,
    relationship_repo,
)
from core.auth.security import require_roles
from core.models.domain import CVE, IOC, Alert, Campaign, Malware, ThreatActor, ThreatEvent
from core.models.enums import Role
from core.models.graph import Relationship
from core.repositories.base import MongoRepository
from core.schemas.pagination import Page

router = APIRouter(tags=["intelligence"])
secured = Depends(require_roles(Role.ADMIN, Role.ANALYST, Role.VIEWER, Role.SERVICE))


async def list_page(
    repo: MongoRepository[Any],
    limit: int,
    offset: int,
    sort: str,
    severity: str | None = None,
) -> Page[Any]:
    query = {"severity": severity} if severity else {}
    items, total = await repo.list(query=query, limit=limit, offset=offset, sort=sort)
    return Page(items=items, total=total, limit=limit, offset=offset)


@router.get("/events", response_model=Page[ThreatEvent], dependencies=[secured])
async def events(
    repo: Annotated[MongoRepository[ThreatEvent], Depends(event_repo)],
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    sort: str = "-created_at",
    severity: str | None = None,
) -> Page[ThreatEvent]:
    return await list_page(repo, limit, offset, sort, severity)


@router.post("/events", response_model=ThreatEvent, dependencies=[Depends(require_roles(Role.ADMIN, Role.SERVICE))])
async def create_event(
    event: ThreatEvent, repo: Annotated[MongoRepository[ThreatEvent], Depends(event_repo)]
) -> ThreatEvent:
    return await repo.upsert(event)


@router.get("/alerts", response_model=Page[Alert], dependencies=[secured])
async def alerts(
    repo: Annotated[MongoRepository[Alert], Depends(alert_repo)], limit: int = 50, offset: int = 0
) -> Page[Alert]:
    return await list_page(repo, limit, offset, "-created_at")


@router.get("/cves", response_model=Page[CVE], dependencies=[secured])
async def cves(repo: Annotated[MongoRepository[CVE], Depends(cve_repo)], limit: int = 50, offset: int = 0) -> Page[CVE]:
    return await list_page(repo, limit, offset, "-created_at")


@router.get("/iocs", response_model=Page[IOC], dependencies=[secured])
async def iocs(repo: Annotated[MongoRepository[IOC], Depends(ioc_repo)], limit: int = 50, offset: int = 0) -> Page[IOC]:
    return await list_page(repo, limit, offset, "-created_at")


@router.get("/actors", response_model=Page[ThreatActor], dependencies=[secured])
async def actors(
    repo: Annotated[MongoRepository[ThreatActor], Depends(actor_repo)], limit: int = 50, offset: int = 0
) -> Page[ThreatActor]:
    return await list_page(repo, limit, offset, "-created_at")


@router.get("/campaigns", response_model=Page[Campaign], dependencies=[secured])
async def campaigns(
    repo: Annotated[MongoRepository[Campaign], Depends(campaign_repo)], limit: int = 50, offset: int = 0
) -> Page[Campaign]:
    return await list_page(repo, limit, offset, "-created_at")


@router.get("/malware", response_model=Page[Malware], dependencies=[secured])
async def malware(
    repo: Annotated[MongoRepository[Malware], Depends(malware_repo)], limit: int = 50, offset: int = 0
) -> Page[Malware]:
    return await list_page(repo, limit, offset, "-created_at")


@router.get("/correlations", response_model=Page[Relationship], dependencies=[secured])
async def correlations(
    repo: Annotated[MongoRepository[Relationship], Depends(relationship_repo)],
    limit: int = 50,
    offset: int = 0,
) -> Page[Relationship]:
    return await list_page(repo, limit, offset, "-created_at")
