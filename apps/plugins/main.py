from apps.collectors.registry import PluginRegistry


async def plugin_health() -> dict[str, object]:
    return {name: health.model_dump() for name, health in (await PluginRegistry().health()).items()}
