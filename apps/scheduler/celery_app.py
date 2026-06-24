from celery import Celery

from core.config.settings import get_settings

settings = get_settings()
celery_app = Celery("threat_nexus", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.beat_schedule = {
    "collect-intelligence-every-15-minutes": {
        "task": "apps.scheduler.tasks.collect_intelligence",
        "schedule": 900,
    },
    "daily-brief": {
        "task": "apps.scheduler.tasks.generate_daily_brief",
        "schedule": 86400,
    },
}
