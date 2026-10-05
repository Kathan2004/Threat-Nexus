from datetime import UTC, datetime
from typing import cast

from motor.motor_asyncio import AsyncIOMotorDatabase

from core.interfaces.plugin import PluginRuntimeConfig
from core.models.source_config import SourceConfig, SourceConfigUpdate, SourceConfigView

SOURCE_CATALOG: dict[str, dict[str, object]] = {
    "cisa-kev": {
        "display_name": "CISA KEV",
        "required_credentials": [],
        "base_url": "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
        "enabled": True,
    },
    "nvd": {
        "display_name": "NVD",
        "required_credentials": [],
        "base_url": "https://services.nvd.nist.gov/rest/json/cves/2.0",
        "enabled": True,
    },
    "virustotal": {
        "display_name": "VirusTotal",
        "required_credentials": ["api_key"],
        "base_url": "https://www.virustotal.com/api/v3",
        "enabled": False,
    },
    "greynoise": {
        "display_name": "GreyNoise",
        "required_credentials": ["api_key"],
        "base_url": "https://api.greynoise.io",
        "enabled": False,
    },
    "abuseipdb": {
        "display_name": "AbuseIPDB",
        "required_credentials": ["api_key"],
        "base_url": "https://api.abuseipdb.com/api/v2",
        "enabled": False,
    },
    "shodan": {
        "display_name": "Shodan",
        "required_credentials": ["api_key"],
        "base_url": "https://api.shodan.io",
        "enabled": False,
    },
    "censys": {
        "display_name": "Censys",
        "required_credentials": ["api_id", "api_secret"],
        "base_url": "https://search.censys.io/api",
        "enabled": False,
    },
    "github": {
        "display_name": "GitHub",
        "required_credentials": ["token"],
        "base_url": "https://api.github.com",
        "enabled": False,
    },
    "reddit": {
        "display_name": "Reddit",
        "required_credentials": ["client_id", "client_secret"],
        "base_url": "https://www.reddit.com",
        "enabled": False,
    },
    "misp": {"display_name": "MISP", "required_credentials": ["api_key"], "base_url": None, "enabled": False},
    "opencti": {"display_name": "OpenCTI", "required_credentials": ["token"], "base_url": None, "enabled": False},
    "intelowl": {"display_name": "IntelOwl", "required_credentials": ["token"], "base_url": None, "enabled": False},
    "alienvault-otx": {
        "display_name": "AlienVault OTX",
        "required_credentials": ["api_key"],
        "base_url": "https://otx.alienvault.com/api/v1",
        "enabled": False,
    },
    "urlhaus": {
        "display_name": "URLHaus",
        "required_credentials": [],
        "base_url": "https://urlhaus-api.abuse.ch/v1",
        "enabled": True,
    },
    "malwarebazaar": {
        "display_name": "MalwareBazaar",
        "required_credentials": [],
        "base_url": "https://mb-api.abuse.ch/api/v1",
        "enabled": True,
    },
    "ransomware-live": {
        "display_name": "Ransomware.live",
        "required_credentials": [],
        "base_url": "https://api.ransomware.live/v2",
        "enabled": True,
    },
    "bleepingcomputer": {
        "display_name": "BleepingComputer",
        "required_credentials": [],
        "base_url": None,
        "enabled": True,
    },
    "the-hacker-news": {
        "display_name": "The Hacker News",
        "required_credentials": [],
        "base_url": None,
        "enabled": True,
    },
    "securityweek": {"display_name": "SecurityWeek", "required_credentials": [], "base_url": None, "enabled": True},
}


class SourceConfigService:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.collection = db["source_configs"]

    async def ensure_indexes(self) -> None:
        await self.collection.create_index("id", unique=True)

    async def list_sources(self) -> list[SourceConfigView]:
        views = []
        for source_id in SOURCE_CATALOG:
            views.append(await self.get_source(source_id))
        return views

    async def get_source(self, source_id: str) -> SourceConfigView:
        if source_id not in SOURCE_CATALOG:
            raise KeyError(source_id)
        stored = await self.collection.find_one({"id": source_id}, {"_id": 0})
        config = SourceConfig.model_validate(stored) if stored else self._default_config(source_id)
        return self._view(config)

    async def get_runtime_configs(self) -> dict[str, PluginRuntimeConfig]:
        configs: dict[str, PluginRuntimeConfig] = {}
        for source_id in SOURCE_CATALOG:
            stored = await self.collection.find_one({"id": source_id}, {"_id": 0})
            config = SourceConfig.model_validate(stored) if stored else self._default_config(source_id)
            catalog = SOURCE_CATALOG[source_id]
            configs[source_id] = PluginRuntimeConfig(
                enabled=config.enabled,
                base_url=config.base_url,
                credentials=config.credentials,
                required_credentials=list(cast(list[str], catalog["required_credentials"])),
                metadata=config.metadata,
            )
        return configs

    async def update_source(self, source_id: str, update: SourceConfigUpdate, actor: str) -> SourceConfigView:
        if source_id not in SOURCE_CATALOG:
            raise KeyError(source_id)
        existing = await self.collection.find_one({"id": source_id}, {"_id": 0})
        config = SourceConfig.model_validate(existing) if existing else self._default_config(source_id)
        if update.enabled is not None:
            config.enabled = update.enabled
        if update.base_url is not None:
            config.base_url = update.base_url.strip() or None
        config.credentials.update({key: value for key, value in update.credentials.items() if value})
        config.metadata.update(update.metadata)
        config.updated_at = datetime.now(UTC)
        config.updated_by = actor
        await self.collection.update_one({"id": source_id}, {"$set": config.model_dump(mode="json")}, upsert=True)
        return self._view(config)

    def _default_config(self, source_id: str) -> SourceConfig:
        catalog = SOURCE_CATALOG[source_id]
        return SourceConfig(
            id=source_id,
            enabled=bool(catalog["enabled"]),
            base_url=catalog["base_url"] if isinstance(catalog["base_url"], str) else None,
        )

    def _view(self, config: SourceConfig) -> SourceConfigView:
        catalog = SOURCE_CATALOG[config.id]
        required = list(cast(list[str], catalog["required_credentials"]))
        configured = sorted(key for key, value in config.credentials.items() if value)
        return SourceConfigView(
            id=config.id,
            display_name=str(catalog["display_name"]),
            enabled=config.enabled,
            base_url=config.base_url,
            required_credentials=required,
            configured_credentials=configured,
            missing_credentials=[key for key in required if key not in configured],
            metadata=config.metadata,
            updated_at=config.updated_at,
            updated_by=config.updated_by,
        )
