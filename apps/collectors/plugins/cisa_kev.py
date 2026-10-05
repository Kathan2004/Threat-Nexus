from typing import Any, cast

from apps.collectors.base_http import HTTPCollectorPlugin


class CISAKEVPlugin(HTTPCollectorPlugin):
    name = "cisa-kev"
    endpoint = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    source_reputation = 96

    async def collect(self) -> list[dict[str, Any]]:
        payload = await super().collect()
        if len(payload) == 1 and "vulnerabilities" in payload[0]:
            return cast(list[dict[str, Any]], payload[0]["vulnerabilities"])
        return payload
