from apps.collectors.base_http import HTTPCollectorPlugin


class MISPPlugin(HTTPCollectorPlugin):
    name = "misp"
    source_reputation = 86

    def auth_headers(self) -> dict[str, str]:
        api_key = self.runtime_config.credentials.get("api_key", "")
        headers = {"Accept": "application/json"}
        if api_key:
            headers["Authorization"] = api_key
        return headers
