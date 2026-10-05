import secrets
import warnings
from functools import lru_cache

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", env_ignore_empty=True
    )

    app_name: str = "Threat Nexus"
    app_env: str = "development"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_database: str = "threat_nexus"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str | None = Field(default=None, min_length=32)
    admin_username: str | None = None
    admin_password: str | None = Field(default=None, min_length=12, max_length=72)
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60
    cors_origins: list[str] = ["http://localhost:3000"]
    discord_token: str | None = None
    discord_guild_id: int | None = None
    openai_api_key: str | None = None
    gemini_api_key: str | None = None
    anthropic_api_key: str | None = None
    cisa_kev_enabled: bool = True
    cisa_kev_url: str = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    nvd_enabled: bool = True
    nvd_api_key: str | None = None
    nvd_base_url: str = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    virustotal_enabled: bool = False
    virustotal_api_key: str | None = None
    virustotal_base_url: str = "https://www.virustotal.com/api/v3"
    greynoise_enabled: bool = False
    greynoise_api_key: str | None = None
    greynoise_base_url: str = "https://api.greynoise.io"
    abuseipdb_enabled: bool = False
    abuseipdb_api_key: str | None = None
    abuseipdb_base_url: str = "https://api.abuseipdb.com/api/v2"
    shodan_enabled: bool = False
    shodan_api_key: str | None = None
    shodan_base_url: str = "https://api.shodan.io"
    censys_enabled: bool = False
    censys_api_id: str | None = None
    censys_api_secret: str | None = None
    censys_base_url: str = "https://search.censys.io/api"
    github_enabled: bool = False
    github_token: str | None = None
    github_base_url: str = "https://api.github.com"
    reddit_enabled: bool = False
    reddit_client_id: str | None = None
    reddit_client_secret: str | None = None
    reddit_user_agent: str = "ThreatNexus/0.1"
    misp_enabled: bool = False
    misp_base_url: str | None = None
    misp_api_key: str | None = None
    misp_verify_tls: bool = True
    opencti_enabled: bool = False
    opencti_base_url: str | None = None
    opencti_token: str | None = None
    intelowl_enabled: bool = False
    intelowl_base_url: str | None = None
    intelowl_token: str | None = None
    otx_enabled: bool = False
    otx_api_key: str | None = None
    otx_base_url: str = "https://otx.alienvault.com/api/v1"
    urlhaus_enabled: bool = True
    urlhaus_base_url: str = "https://urlhaus-api.abuse.ch/v1"
    malwarebazaar_enabled: bool = True
    malwarebazaar_base_url: str = "https://mb-api.abuse.ch/api/v1"
    ransomware_live_enabled: bool = True
    ransomware_live_base_url: str = "https://api.ransomware.live/v2"
    bleepingcomputer_enabled: bool = True
    the_hacker_news_enabled: bool = True
    securityweek_enabled: bool = True

    @model_validator(mode="after")
    def _require_strong_jwt_secret(self) -> "Settings":
        weak = {None, "change-me-with-a-32-byte-secret"}
        if self.jwt_secret in weak:
            if self.app_env != "development":
                raise ValueError("JWT_SECRET must be set to a random value of at least 32 characters")
            warnings.warn(
                "JWT_SECRET not set; using a random per-process secret (tokens reset on restart).",
                stacklevel=2,
            )
            self.jwt_secret = secrets.token_urlsafe(48)
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
