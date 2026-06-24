from apps.collectors.base_http import HTTPCollectorPlugin


class VirusTotalPlugin(HTTPCollectorPlugin):
    name = "virustotal"
    source_reputation = 84

    def auth_headers(self) -> dict[str, str]:
        api_key = self.runtime_config.credentials.get("api_key", "")
        return {"x-apikey": api_key} if api_key else {}
