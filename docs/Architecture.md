# Architecture

Threat Nexus is organized as a modular intelligence platform with shared domain code in `core/` and deployable services in `apps/`.

The ingestion path is:

1. Collector plugins fetch raw source data.
2. Plugins normalize raw items into internal `ThreatEvent` objects.
3. Aggregation merges observations and preserves source attribution.
4. Deduplication prevents repeated storage and repeated Discord alerts.
5. Confidence and scoring services assign confidence and severity.
6. Correlation builds relationship records for graph traversal.
7. Enrichment adds structured analyst-ready summaries.
8. Alerts route enriched intelligence to API consumers and Discord.

Service boundaries are intentionally thin. Business logic lives in `core/services` and storage access lives in `core/repositories`, which keeps API, Discord, Celery, and future workers from duplicating behavior.
