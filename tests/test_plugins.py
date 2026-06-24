import pytest

from apps.collectors.plugins.virustotal import VirusTotalPlugin
from apps.collectors.registry import PluginRegistry
from core.interfaces.plugin import PluginRuntimeConfig


def test_registry_discovers_builtin_plugins() -> None:
    plugins = PluginRegistry().discover()

    assert "cisa-kev" in plugins
    assert "virustotal" in plugins
    assert "ransomware-live" in plugins


@pytest.mark.asyncio
async def test_plugin_reports_missing_required_runtime_credentials() -> None:
    plugin = VirusTotalPlugin()
    plugin.configure(
        PluginRuntimeConfig(
            enabled=True,
            base_url="https://www.virustotal.com/api/v3",
            required_credentials=["api_key"],
        )
    )

    health = await plugin.health_check()

    assert not health.healthy
    assert health.details["status"] == "missing_credentials"
