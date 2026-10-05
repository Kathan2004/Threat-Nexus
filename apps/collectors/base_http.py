from datetime import UTC, datetime
from typing import Any, cast

import httpx

from core.interfaces.plugin import CollectorPlugin, PluginHealth
from core.models.base import SourceAttribution
from core.models.domain import CVE, IOC, ThreatEvent
from core.models.enums import IOCType, Severity


class HTTPCollectorPlugin(CollectorPlugin):
    name = "base-http"
    version = "1.0.0"
    source_reputation = 50
    endpoint: str | None = None
    timeout_seconds = 15

    async def collect(self) -> list[dict[str, Any]]:
        if not self.runtime_config.enabled:
            return []
        if self.runtime_config.missing_credentials:
            return []
        endpoint = self.collection_endpoint()
        if not endpoint:
            return []
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.get(endpoint, headers=self.auth_headers(), auth=self.auth())
            response.raise_for_status()
            payload = response.json()
        if isinstance(payload, list):
            return cast(list[dict[str, Any]], payload)
        if isinstance(payload, dict):
            for key in ("items", "data", "results", "vulnerabilities"):
                if isinstance(payload.get(key), list):
                    return cast(list[dict[str, Any]], payload[key])
            return [payload]
        return []

    async def normalize(self, raw: dict[str, Any]) -> ThreatEvent:
        title = str(raw.get("title") or raw.get("name") or raw.get("cveID") or f"{self.name} intelligence")
        description = str(raw.get("description") or raw.get("summary") or raw.get("details") or title)
        source = SourceAttribution(
            source=self.name, url=raw.get("url"), confidence=self.source_reputation, raw_reference=raw
        )
        event = ThreatEvent(title=title, description=description, severity=Severity.MEDIUM, sources=[source])
        if cve_id := raw.get("cveID") or raw.get("cve_id") or raw.get("id"):
            if isinstance(cve_id, str) and cve_id.upper().startswith("CVE-"):
                event.cves.append(
                    CVE(
                        cve_id=cve_id.upper(),
                        title=title,
                        description=description,
                        kev=bool(raw.get("knownRansomwareCampaignUse") or raw.get("kev")),
                        active_exploitation=bool(raw.get("active_exploitation") or raw.get("dateAdded")),
                        sources=[source],
                    )
                )
        for value in raw.get("iocs", []) if isinstance(raw.get("iocs"), list) else []:
            if isinstance(value, str):
                event.iocs.append(IOC(type=self._infer_ioc_type(value), value=value, sources=[source]))
        event.updated_at = datetime.now(UTC)
        return event

    async def validate(self, event: ThreatEvent) -> bool:
        return bool(event.title and event.description and event.sources)

    async def health_check(self) -> PluginHealth:
        if not self.runtime_config.enabled:
            return PluginHealth(healthy=True, details={"status": "disabled"})
        if self.runtime_config.missing_credentials:
            return PluginHealth(
                healthy=False,
                details={"status": "missing_credentials", "missing": self.runtime_config.missing_credentials},
            )
        endpoint = self.collection_endpoint()
        if not endpoint:
            return PluginHealth(healthy=True, details={"mode": "configured-without-endpoint"})
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                auth = self.auth()
                response = await client.head(
                    endpoint, headers=self.auth_headers(), auth=auth if auth is not None else httpx.USE_CLIENT_DEFAULT
                )
            return PluginHealth(healthy=response.status_code < 500, details={"status_code": response.status_code})
        except Exception as exc:
            return PluginHealth(healthy=False, details={"error": str(exc)})

    def collection_endpoint(self) -> str | None:
        return self.runtime_config.base_url or self.endpoint

    def auth_headers(self) -> dict[str, str]:
        credentials = self.runtime_config.credentials
        if api_key := credentials.get("api_key"):
            return {"Authorization": f"Bearer {api_key}"}
        if token := credentials.get("token"):
            return {"Authorization": f"Bearer {token}"}
        return {}

    def auth(self) -> httpx.Auth | None:
        return None

    def _infer_ioc_type(self, value: str) -> IOCType:
        lowered = value.lower()
        if len(lowered) == 64 and all(char in "0123456789abcdef" for char in lowered):
            return IOCType.SHA256
        if len(lowered) == 32 and all(char in "0123456789abcdef" for char in lowered):
            return IOCType.MD5
        if "@" in lowered:
            return IOCType.EMAIL
        if lowered.startswith(("http://", "https://")):
            return IOCType.URL
        if all(part.isdigit() for part in lowered.split(".") if part) and lowered.count(".") == 3:
            return IOCType.IP
        return IOCType.DOMAIN
