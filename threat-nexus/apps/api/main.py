from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from starlette.responses import JSONResponse

from apps.api.routers import auth, crud, dashboard, search, settings as settings_router
from core.config.settings import get_settings
from core.database.mongo import mongo
from core.logging.config import configure_logging
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
from core.services.source_config import SourceConfigService


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
    yield
    await mongo.close()


settings = get_settings()
limiter = Limiter(key_func=get_remote_address, default_limits=["120/minute"])
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
    allow_methods=["*"],
    allow_headers=["*"],
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
