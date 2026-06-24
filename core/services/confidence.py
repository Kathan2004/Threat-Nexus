from core.models.domain import ThreatEvent


class ConfidenceService:
    def calculate(self, event: ThreatEvent) -> int:
        source_count = len({source.source for source in event.sources})
        source_reputation = max([source.confidence for source in event.sources], default=35)
        corroboration = min(source_count * 10, 30)
        exploitation = 15 if event.active_exploitation else 0
        indicator_bonus = min(len(event.iocs) + len(event.cves), 10)
        return max(0, min(100, source_reputation + corroboration + exploitation + indicator_bonus))
