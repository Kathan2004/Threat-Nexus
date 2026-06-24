from collections.abc import Iterable

from core.models.domain import ThreatEvent
from core.services.confidence import ConfidenceService
from core.services.deduplication import DeduplicationService
from core.services.scoring import ThreatScoringService


class AggregationService:
    def __init__(
        self,
        deduplication: DeduplicationService | None = None,
        confidence: ConfidenceService | None = None,
        scoring: ThreatScoringService | None = None,
    ) -> None:
        self.deduplication = deduplication or DeduplicationService()
        self.confidence = confidence or ConfidenceService()
        self.scoring = scoring or ThreatScoringService()

    def merge(self, events: Iterable[ThreatEvent]) -> list[ThreatEvent]:
        merged: list[ThreatEvent] = []
        for event in events:
            match = next((item for item in merged if self.deduplication.is_duplicate(item, event)), None)
            if match:
                self._merge_into(match, event)
            else:
                merged.append(event)
        for event in merged:
            event.confidence = self.confidence.calculate(event)
            event.severity = self.scoring.score(event)
        return merged

    def _merge_into(self, target: ThreatEvent, incoming: ThreatEvent) -> None:
        target.description = max([target.description, incoming.description], key=len)
        target.active_exploitation = target.active_exploitation or incoming.active_exploitation
        target.sources.extend(source for source in incoming.sources if source not in target.sources)
        target.iocs.extend(ioc for ioc in incoming.iocs if ioc.value not in {existing.value for existing in target.iocs})
        target.cves.extend(cve for cve in incoming.cves if cve.cve_id not in {existing.cve_id for existing in target.cves})
        target.threat_actor_ids = sorted(set(target.threat_actor_ids + incoming.threat_actor_ids))
        target.campaign_ids = sorted(set(target.campaign_ids + incoming.campaign_ids))
        target.malware_ids = sorted(set(target.malware_ids + incoming.malware_ids))
        target.victim_ids = sorted(set(target.victim_ids + incoming.victim_ids))
        target.touch()
