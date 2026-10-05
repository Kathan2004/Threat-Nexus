import httpx

from apps.collectors.base_http import HTTPCollectorPlugin


class CensysPlugin(HTTPCollectorPlugin):
    name = "censys"
    source_reputation = 78

    def auth(self) -> httpx.BasicAuth | None:
        api_id = self.runtime_config.credentials.get("api_id")
        api_secret = self.runtime_config.credentials.get("api_secret")
        if api_id and api_secret:
            return httpx.BasicAuth(api_id, api_secret)
        return None
