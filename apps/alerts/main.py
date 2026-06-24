from core.models.domain import Alert, ThreatEvent

CHANNELS = {
    "CRITICAL": ["critical-alerts", "intel-feed"],
    "HIGH": ["intel-feed", "cve-watch"],
    "MEDIUM": ["intel-feed"],
    "LOW": ["analyst-room"],
}


class AlertService:
    def build_alert(self, event: ThreatEvent) -> Alert:
        return Alert(
            event_id=event.id,
            title=event.title,
            severity=event.severity,
            confidence=event.confidence,
            channels=CHANNELS[event.severity.value],
        )
