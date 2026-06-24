from apps.collectors.base_http import HTTPCollectorPlugin


class IntelOwlPlugin(HTTPCollectorPlugin):
    name = "intelowl"
    source_reputation = 82

    def auth_headers(self) -> dict[str, str]:
        token = self.runtime_config.credentials.get("token", "")
        return {"Authorization": f"Token {token}"} if token else {}
