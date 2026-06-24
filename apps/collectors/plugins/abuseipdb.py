from apps.collectors.base_http import HTTPCollectorPlugin


class AbuseIPDBPlugin(HTTPCollectorPlugin):
    name = "abuseipdb"
    source_reputation = 78

    def auth_headers(self) -> dict[str, str]:
        api_key = self.runtime_config.credentials.get("api_key", "")
        return {"Key": api_key, "Accept": "application/json"} if api_key else {"Accept": "application/json"}
