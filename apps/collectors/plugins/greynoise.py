from apps.collectors.base_http import HTTPCollectorPlugin


class GreyNoisePlugin(HTTPCollectorPlugin):
    name = "greynoise"
    source_reputation = 83

    def auth_headers(self) -> dict[str, str]:
        api_key = self.runtime_config.credentials.get("api_key", "")
        return {"key": api_key} if api_key else {}
