from core.models.domain import ThreatEvent


class NormalizationService:
    def normalize(self, event: ThreatEvent) -> ThreatEvent:
        event.title = event.title.strip()
        event.description = event.description.strip()
        return event
