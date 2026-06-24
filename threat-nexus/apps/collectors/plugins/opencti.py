from apps.collectors.base_http import HTTPCollectorPlugin


class OpenCTIPlugin(HTTPCollectorPlugin):
    name = "opencti"
    source_reputation = 88

    def auth_headers(self) -> dict[str, str]:
        token = self.runtime_config.credentials.get("token", "")
        return {"Authorization": f"Bearer {token}"} if token else {}
