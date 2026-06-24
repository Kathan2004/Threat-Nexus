from datetime import UTC, datetime

from pydantic import Field, field_validator

from core.models.base import Entity, SourceAttribution
from core.models.enums import IOCType, Severity


class IOC(Entity):
    type: IOCType
    value: str
    sources: list[SourceAttribution] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    first_seen: datetime | None = None
    last_seen: datetime | None = None

    @field_validator("value")
    @classmethod
    def normalize_value(cls, value: str) -> str:
        return value.strip().lower()


class CVE(Entity):
    cve_id: str
    title: str
    description: str
    cvss: float | None = Field(default=None, ge=0, le=10)
    kev: bool = False
    public_exploit: bool = False
    active_exploitation: bool = False
    affected_products: list[str] = Field(default_factory=list)
    sources: list[SourceAttribution] = Field(default_factory=list)


class ThreatActor(Entity):
    name: str
    aliases: list[str] = Field(default_factory=list)
    motivations: list[str] = Field(default_factory=list)
    countries: list[str] = Field(default_factory=list)
    sources: list[SourceAttribution] = Field(default_factory=list)


class Campaign(Entity):
    name: str
    description: str = ""
    threat_actor_ids: list[str] = Field(default_factory=list)
    malware_ids: list[str] = Field(default_factory=list)
    start_time: datetime | None = None
    end_time: datetime | None = None
    sources: list[SourceAttribution] = Field(default_factory=list)


class Malware(Entity):
    name: str
    aliases: list[str] = Field(default_factory=list)
    families: list[str] = Field(default_factory=list)
    capabilities: list[str] = Field(default_factory=list)
    sources: list[SourceAttribution] = Field(default_factory=list)


class Victim(Entity):
    name: str
    sectors: list[str] = Field(default_factory=list)
    countries: list[str] = Field(default_factory=list)
    sources: list[SourceAttribution] = Field(default_factory=list)


class Tool(Entity):
    name: str
    description: str = ""
    sources: list[SourceAttribution] = Field(default_factory=list)


class Technique(Entity):
    mitre_id: str
    name: str
    tactic: str | None = None
    sources: list[SourceAttribution] = Field(default_factory=list)


class AIEnrichment(Entity):
    executive_summary: str
    technical_analysis: str
    affected_assets: list[str] = Field(default_factory=list)
    mitre_attack: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    detection_opportunities: list[str] = Field(default_factory=list)
    analyst_notes: list[str] = Field(default_factory=list)
    confidence_explanation: str


class ThreatEvent(Entity):
    title: str
    description: str
    severity: Severity = Severity.MEDIUM
    confidence: int = Field(ge=0, le=100, default=50)
    active_exploitation: bool = False
    iocs: list[IOC] = Field(default_factory=list)
    cves: list[CVE] = Field(default_factory=list)
    threat_actor_ids: list[str] = Field(default_factory=list)
    campaign_ids: list[str] = Field(default_factory=list)
    malware_ids: list[str] = Field(default_factory=list)
    victim_ids: list[str] = Field(default_factory=list)
    sources: list[SourceAttribution] = Field(default_factory=list)
    enrichment: AIEnrichment | None = None
    published_to_discord: bool = False


class Alert(Entity):
    event_id: str
    title: str
    severity: Severity
    confidence: int = Field(ge=0, le=100)
    channels: list[str] = Field(default_factory=list)
    message_id: str | None = None
    thread_id: str | None = None
    published_at: datetime | None = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
