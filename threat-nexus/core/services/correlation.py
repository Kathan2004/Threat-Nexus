from core.models.domain import ThreatEvent
from core.models.graph import Relationship


class CorrelationService:
    def correlate(self, event: ThreatEvent) -> list[Relationship]:
        relationships: list[Relationship] = []
        for cve in event.cves:
            relationships.append(self._rel(event.id, "ThreatEvent", cve.id, "CVE", "mentions"))
        for ioc in event.iocs:
            relationships.append(self._rel(event.id, "ThreatEvent", ioc.id, "IOC", "observes"))
        for actor_id in event.threat_actor_ids:
            relationships.append(self._rel(actor_id, "ThreatActor", event.id, "ThreatEvent", "associated_with"))
        for malware_id in event.malware_ids:
            relationships.append(self._rel(malware_id, "Malware", event.id, "ThreatEvent", "used_in"))
        return relationships

    def _rel(self, source_id: str, source_type: str, target_id: str, target_type: str, relation: str) -> Relationship:
        return Relationship(
            source_id=source_id,
            source_type=source_type,
            target_id=target_id,
            target_type=target_type,
            relation=relation,
            score=0.75,
        )
