from apps.collectors.base_http import HTTPCollectorPlugin


class GitHubSecurityPlugin(HTTPCollectorPlugin):
    name = "github"
    source_reputation = 74

    def auth_headers(self) -> dict[str, str]:
        token = self.runtime_config.credentials.get("token", "")
        headers = {"Accept": "application/vnd.github+json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers
