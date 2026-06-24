from core.models.domain import ThreatEvent
from core.models.enums import Severity


class ThreatScoringService:
    def score(self, event: ThreatEvent) -> Severity:
        points = 0
        points += 30 if event.active_exploitation else 0
        points += 15 if event.threat_actor_ids else 0
        points += 15 if event.malware_ids else 0
        points += 10 if any("ransomware" in tag for ioc in event.iocs for tag in ioc.tags) else 0
        for cve in event.cves:
            points += 20 if cve.kev else 0
            points += 15 if cve.public_exploit else 0
            points += 20 if cve.cvss and cve.cvss >= 9 else 0
            points += 10 if cve.cvss and cve.cvss >= 7 else 0
        if points >= 70:
            return Severity.CRITICAL
        if points >= 45:
            return Severity.HIGH
        if points >= 20:
            return Severity.MEDIUM
        return Severity.LOW
