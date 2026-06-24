from core.models.base import SourceAttribution
from core.models.domain import CVE, IOC, ThreatEvent
from core.models.enums import IOCType
from core.services.deduplication import DeduplicationService


def test_exact_fingerprint_matches_for_same_cve_and_ioc() -> None:
    source = SourceAttribution(source="unit-test", confidence=80)
    left = ThreatEvent(
        title="Edge device exploited",
        description="Observed exploitation",
        cves=[CVE(cve_id="CVE-2026-0001", title="cve", description="desc", sources=[source])],
        iocs=[IOC(type=IOCType.DOMAIN, value="evil.example", sources=[source])],
        sources=[source],
    )
    right = ThreatEvent(
        title="Edge device exploited",
        description="Observed exploitation",
        cves=[CVE(cve_id="CVE-2026-0001", title="cve", description="desc", sources=[source])],
        iocs=[IOC(type=IOCType.DOMAIN, value="evil.example", sources=[source])],
        sources=[source],
    )

    assert DeduplicationService().is_duplicate(left, right)
