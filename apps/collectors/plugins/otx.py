from apps.collectors.base_http import HTTPCollectorPlugin


class AlienVaultOTXPlugin(HTTPCollectorPlugin):
    name = "alienvault-otx"
    source_reputation = 78

    def auth_headers(self) -> dict[str, str]:
        api_key = self.runtime_config.credentials.get("api_key", "")
        return {"X-OTX-API-KEY": api_key} if api_key else {}
