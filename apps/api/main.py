import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.responses import JSONResponse

from apps.api.ratelimit import limiter
from apps.api.routers import auth, crud, dashboard, search
from apps.api.routers import settings as settings_router
from core.auth.users import UserRepository
from core.config.settings import get_settings
from core.database.mongo import mongo
from core.logging.config import configure_logging
from core.models.enums import Role
from core.repositories.intel import (
    ActorRepository,
    AlertRepository,
    CampaignRepository,
    CVERepository,
    EventRepository,
    IOCRepository,
    MalwareRepository,
    RelationshipRepository,
)
from core.services.source_config import SourceConfigService


async def bootstrap_admin(users: UserRepository) -> None:
    """Create the first admin from ADMIN_USERNAME/ADMIN_PASSWORD when no users exist."""
    await users.ensure_indexes()
    if await users.count():
        return
    settings = get_settings()
    if not (settings.admin_username and settings.admin_password):
        logger.warning("No users exist. Set ADMIN_USERNAME and ADMIN_PASSWORD to create the first admin.")
        return
    await users.create(settings.admin_username, settings.admin_password, {Role.ADMIN})
    logger.info("Bootstrapped admin user %s", settings.admin_username)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    for repo in (
        EventRepository(mongo.db),
        IOCRepository(mongo.db),
        CVERepository(mongo.db),
        ActorRepository(mongo.db),
        CampaignRepository(mongo.db),
        MalwareRepository(mongo.db),
        AlertRepository(mongo.db),
        RelationshipRepository(mongo.db),
    ):
        await repo.ensure_indexes()
    await SourceConfigService(mongo.db).ensure_indexes()
    await bootstrap_admin(UserRepository(mongo.db))
    yield
    await mongo.close()


logger = logging.getLogger(__name__)
settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    lambda _, exc: JSONResponse(status_code=429, content={"detail": f"Rate limit exceeded: {exc.detail}"}),
)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
app.include_router(auth.router)
app.include_router(crud.router)
app.include_router(search.router)
app.include_router(dashboard.router)
app.include_router(settings_router.router)
app.mount("/metrics", make_asgi_app())


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
