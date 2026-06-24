from core.models.base import SourceAttribution
from core.models.domain import IOC, ThreatEvent
from core.models.enums import IOCType, Severity
from core.services.aggregation import AggregationService


def test_aggregation_merges_duplicate_events_and_scores() -> None:
    first_source = SourceAttribution(source="cisa-kev", confidence=95)
    second_source = SourceAttribution(source="greynoise", confidence=80)
    first = ThreatEvent(
        title="Mass exploitation campaign",
        description="Short",
        active_exploitation=True,
        iocs=[IOC(type=IOCType.IP, value="203.0.113.10", sources=[first_source])],
        sources=[first_source],
    )
    second = ThreatEvent(
        title="Mass exploitation campaign observed",
        description="Longer technical description",
        active_exploitation=True,
        iocs=[IOC(type=IOCType.IP, value="203.0.113.10", sources=[second_source])],
        sources=[second_source],
    )

    merged = AggregationService().merge([first, second])

    assert len(merged) == 1
    assert merged[0].confidence >= 95
    assert merged[0].severity in {Severity.MEDIUM, Severity.HIGH, Severity.CRITICAL}
    assert {source.source for source in merged[0].sources} == {"cisa-kev", "greynoise"}
