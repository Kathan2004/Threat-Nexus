import hashlib

from rapidfuzz import fuzz

from core.models.domain import ThreatEvent


class DeduplicationService:
    exact_ioc_types = {"cve", "sha256", "md5", "ip", "domain", "url", "email"}

    def fingerprint(self, event: ThreatEvent) -> str:
        cves = sorted(cve.cve_id.upper() for cve in event.cves)
        iocs = sorted(f"{ioc.type}:{ioc.value}" for ioc in event.iocs)
        material = "|".join([event.title.strip().lower(), *cves, *iocs])
        return hashlib.sha256(material.encode("utf-8")).hexdigest()

    def fuzzy_match(self, left: ThreatEvent, right: ThreatEvent) -> float:
        title = fuzz.token_set_ratio(left.title, right.title) / 100
        description = fuzz.token_set_ratio(left.description, right.description) / 100
        overlap = self._ioc_overlap(left, right)
        return max(title * 0.45 + description * 0.35 + overlap * 0.20, overlap)

    def is_duplicate(self, left: ThreatEvent, right: ThreatEvent, threshold: float = 0.88) -> bool:
        if self.fingerprint(left) == self.fingerprint(right):
            return True
        return self.fuzzy_match(left, right) >= threshold

    def _ioc_overlap(self, left: ThreatEvent, right: ThreatEvent) -> float:
        a = {f"{ioc.type}:{ioc.value}" for ioc in left.iocs} | {cve.cve_id for cve in left.cves}
        b = {f"{ioc.type}:{ioc.value}" for ioc in right.iocs} | {cve.cve_id for cve in right.cves}
        if not a or not b:
            return 0
        return len(a & b) / len(a | b)
