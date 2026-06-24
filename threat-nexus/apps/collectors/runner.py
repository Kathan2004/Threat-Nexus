import asyncio

import structlog

from apps.collectors.registry import PluginRegistry
from core.database.mongo import mongo
from core.services.aggregation import AggregationService
from core.services.source_config import SourceConfigService

logger = structlog.get_logger()


async def collect_once() -> list[str]:
    registry = PluginRegistry()
    aggregator = AggregationService()
    source_config_service = SourceConfigService(mongo.db)
    await source_config_service.ensure_indexes()
    runtime_configs = await source_config_service.get_runtime_configs()
    events = []
    for plugin in registry.all():
        try:
            if runtime_config := runtime_configs.get(plugin.name):
                plugin.configure(runtime_config)
            health = await plugin.health_check()
            if not health.healthy:
                logger.warning("plugin_unhealthy", plugin=plugin.name, details=health.details)
                continue
            raw_items = await plugin.collect()
            for raw in raw_items:
                event = await plugin.normalize(raw)
                if await plugin.validate(event):
                    events.append(event)
        except Exception as exc:
            logger.warning("plugin_collection_failed", plugin=plugin.name, error=str(exc))
    merged = aggregator.merge(events)
    return [event.id for event in merged]


def main() -> None:
    asyncio.run(collect_once())


if __name__ == "__main__":
    main()
