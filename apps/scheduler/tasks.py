import asyncio

from apps.collectors.runner import collect_once
from apps.scheduler.celery_app import celery_app


@celery_app.task(name="apps.scheduler.tasks.collect_intelligence")
def collect_intelligence() -> list[str]:
    return asyncio.run(collect_once())


@celery_app.task(name="apps.scheduler.tasks.generate_daily_brief")
def generate_daily_brief() -> dict[str, str]:
    return {"status": "queued"}
