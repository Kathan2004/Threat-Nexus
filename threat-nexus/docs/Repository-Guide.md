# Repository Guide

This guide explains the Threat Nexus project layout from the top down. Read this first if you are new to the codebase.

## Big Picture

Threat Nexus is split into three main areas:

- `core/`: shared backend logic used by every service.
- `apps/`: runnable backend services and service-specific entrypoints.
- `frontend/`: the web interface analysts use.

Most real business rules live in `core/services/`. The files in `apps/` usually wire those rules into an API, worker, Discord bot, scheduler, or plugin runner.

## Full Directory Tree

```text
threat-nexus/
├── .env
├── .env.example
├── .github/
│   └── workflows/
│       └── ci.yml
├── README.md
├── apps/
│   ├── __init__.py
│   ├── aggregation/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── alerts/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   ├── main.py
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── crud.py
│   │       ├── dashboard.py
│   │       └── search.py
│   ├── audit/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── collectors/
│   │   ├── __init__.py
│   │   ├── base_http.py
│   │   ├── registry.py
│   │   ├── runner.py
│   │   └── plugins/
│   │       ├── __init__.py
│   │       ├── abuseipdb.py
│   │       ├── censys.py
│   │       ├── cisa_kev.py
│   │       ├── github.py
│   │       ├── greynoise.py
│   │       ├── intelowl.py
│   │       ├── malwarebazaar.py
│   │       ├── misp.py
│   │       ├── news.py
│   │       ├── nvd.py
│   │       ├── opencti.py
│   │       ├── otx.py
│   │       ├── ransomware_live.py
│   │       ├── reddit.py
│   │       ├── shodan.py
│   │       ├── urlhaus.py
│   │       └── virustotal.py
│   ├── confidence/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── correlation/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── deduplication/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── discord_bot/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── publisher.py
│   ├── enrichment/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── graph/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── normalization/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── plugins/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── scheduler/
│   │   ├── __init__.py
│   │   ├── celery_app.py
│   │   └── tasks.py
│   ├── scoring/
│   │   ├── __init__.py
│   │   └── main.py
│   └── search/
│       ├── __init__.py
│       └── main.py
├── core/
│   ├── __init__.py
│   ├── auth/
│   │   └── security.py
│   ├── config/
│   │   └── settings.py
│   ├── database/
│   │   ├── mongo.py
│   │   └── redis.py
│   ├── interfaces/
│   │   └── plugin.py
│   ├── logging/
│   │   └── config.py
│   ├── models/
│   │   ├── base.py
│   │   ├── domain.py
│   │   ├── enums.py
│   │   └── graph.py
│   ├── repositories/
│   │   ├── base.py
│   │   └── intel.py
│   ├── schemas/
│   │   └── pagination.py
│   └── services/
│       ├── aggregation.py
│       ├── audit.py
│       ├── confidence.py
│       ├── correlation.py
│       ├── deduplication.py
│       ├── enrichment.py
│       ├── scoring.py
│       └── search.py
├── docker/
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
├── docker-compose.yml
├── docs/
│   ├── API.md
│   ├── Architecture.md
│   ├── Deployment.md
│   ├── Developer.md
│   ├── Plugin-Development-Guide.md
│   └── Repository-Guide.md
├── frontend/
│   ├── app/
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── next.config.ts
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.ts
│   └── tsconfig.json
├── infra/
│   ├── grafana-dashboard.json
│   └── prometheus.yml
├── pyproject.toml
├── scripts/
│   ├── bootstrap.sh
│   └── run-api.sh
└── tests/
    ├── test_aggregation.py
    ├── test_api.py
    ├── test_deduplication.py
    └── test_plugins.py
```

## Root Files

### `.env`

Local environment variables. This file is used when running the project on your machine or through Docker Compose. It can contain secrets, so do not commit real production values.

### `.env.example`

Safe example environment file. Use this as the template for creating `.env`.

### `README.md`

The project overview. It gives the shortest introduction, local start command, and high-level roadmap.

### `pyproject.toml`

Python project configuration. It declares backend dependencies, developer dependencies, package metadata, pytest config, Ruff lint config, and mypy type-checking config.

### `docker-compose.yml`

Local multi-service stack. It starts MongoDB, Redis, the API, Celery scheduler/worker, Discord service, frontend, Prometheus, and Grafana.

## `.github/`

GitHub automation lives here.

### `.github/workflows/ci.yml`

Continuous integration workflow. It installs Python and Node dependencies, runs backend linting, type checks, tests, and frontend linting.

## `apps/`

This directory contains runnable backend services or service-specific adapters. Think of these as the outer shell of the backend.

### `apps/api/`

FastAPI service. This is the HTTP API used by the frontend, external tools, and operators.

- `main.py`: creates the FastAPI app, configures CORS, rate limiting, metrics, routers, startup index creation, and `/health`.
- `dependencies.py`: FastAPI dependency functions that provide repositories to route handlers.
- `routers/auth.py`: token endpoint for JWT generation.
- `routers/crud.py`: REST endpoints for events, alerts, CVEs, actors, campaigns, malware, IOCs, and correlations.
- `routers/dashboard.py`: dashboard and analytics summary endpoints.
- `routers/search.py`: full-text search endpoint.

### `apps/collectors/`

Collector service and plugin loader. This is where external intelligence sources enter the platform.

- `base_http.py`: reusable HTTP collector base class. It fetches JSON, normalizes common fields, infers IOC types, and performs basic health checks.
- `registry.py`: discovers collector plugins automatically from `apps.collectors.plugins`.
- `runner.py`: runs all discovered plugins, normalizes items into `ThreatEvent` objects, validates them, and sends them through aggregation.
- `plugins/`: one module per intelligence source or source family.

Plugin files:

- `abuseipdb.py`: AbuseIPDB connector class.
- `censys.py`: Censys connector class.
- `cisa_kev.py`: CISA Known Exploited Vulnerabilities connector with a real public endpoint.
- `github.py`: GitHub security intelligence connector class.
- `greynoise.py`: GreyNoise connector class.
- `intelowl.py`: IntelOwl connector class.
- `malwarebazaar.py`: MalwareBazaar connector class.
- `misp.py`: MISP connector class.
- `news.py`: BleepingComputer, The Hacker News, and SecurityWeek connector classes.
- `nvd.py`: NVD CVE connector class.
- `opencti.py`: OpenCTI connector class.
- `otx.py`: AlienVault OTX connector class.
- `ransomware_live.py`: Ransomware.live connector class.
- `reddit.py`: Reddit connector class.
- `shodan.py`: Shodan connector class.
- `urlhaus.py`: URLHaus connector class.
- `virustotal.py`: VirusTotal connector class.

### `apps/aggregation/`

Service wrapper for aggregation logic.

- `main.py`: exposes `AggregationService` from `core.services.aggregation`.

### `apps/normalization/`

Normalization service wrapper.

- `main.py`: contains a small normalization service that trims normalized event text.

### `apps/deduplication/`

Deduplication service wrapper.

- `main.py`: exposes `DeduplicationService`.

### `apps/correlation/`

Correlation service wrapper.

- `main.py`: exposes `CorrelationService`.

### `apps/confidence/`

Confidence service wrapper.

- `main.py`: exposes `ConfidenceService`.

### `apps/enrichment/`

AI enrichment service wrapper.

- `main.py`: exposes `EnrichmentService`.

### `apps/scoring/`

Threat scoring service wrapper.

- `main.py`: exposes `ThreatScoringService`.

### `apps/alerts/`

Alert creation and routing logic.

- `main.py`: maps event severity to Discord/API alert channels and builds `Alert` objects.

### `apps/discord_bot/`

Discord integration service.

- `main.py`: creates and runs the Discord client.
- `publisher.py`: converts enriched `ThreatEvent` objects into Discord embeds and updates or creates messages/threads.

### `apps/scheduler/`

Celery scheduler and task runner.

- `celery_app.py`: configures Celery, Redis broker/backend, and scheduled jobs.
- `tasks.py`: Celery tasks for intelligence collection and daily brief generation.

### `apps/plugins/`

Plugin service facade.

- `main.py`: exposes plugin health information using the collector plugin registry.

### `apps/search/`

Search service wrapper.

- `main.py`: re-exports `SearchService`.

### `apps/graph/`

Knowledge graph service wrapper.

- `main.py`: contains graph neighbor traversal over relationship records.

### `apps/audit/`

Audit service wrapper.

- `main.py`: re-exports `AuditService`.

## `core/`

This is the shared backend library. Anything here should be independent of FastAPI, Discord, or Celery unless it is specifically an integration helper.

### `core/config/`

Application configuration.

- `settings.py`: Pydantic Settings model. Reads environment variables such as MongoDB URI, Redis URL, JWT secret, Discord token, and AI provider keys.

### `core/auth/`

Authentication and authorization.

- `security.py`: password hashing helpers, JWT creation, token parsing, principal model, and RBAC dependency helpers.

### `core/database/`

Database clients.

- `mongo.py`: Motor/MongoDB client and FastAPI database dependency.
- `redis.py`: Redis client factory.

### `core/interfaces/`

Abstract contracts that other code must implement.

- `plugin.py`: `CollectorPlugin` interface, runtime plugin config model, and `PluginHealth` model. Every intelligence plugin must implement this contract.

### `core/logging/`

Logging setup.

- `config.py`: configures structured JSON logging with `structlog`.

### `core/models/`

Domain models. These define the internal language of the platform.

- `base.py`: shared entity fields such as `id`, timestamps, and source attribution.
- `domain.py`: main intelligence models: `ThreatEvent`, `ThreatActor`, `Campaign`, `Malware`, `IOC`, `CVE`, `Alert`, `Victim`, `Tool`, `Technique`, and `AIEnrichment`.
- `enums.py`: shared enums such as severity, IOC type, confidence level, and user role.
- `graph.py`: relationship model for the knowledge graph.

### `core/repositories/`

Persistence layer.

- `base.py`: generic Mongo repository with upsert, get, find, and list behavior.
- `intel.py`: typed repositories for events, IOCs, CVEs, actors, campaigns, malware, alerts, and relationships.

### `core/schemas/`

API and transport schemas that are not core domain objects.

- `pagination.py`: generic paginated response model.

### `core/services/`

Business logic.

- `aggregation.py`: merges duplicate or related threat events while preserving source attribution.
- `audit.py`: writes audit log records.
- `confidence.py`: calculates 0-100 confidence scores from source reputation, corroboration, exploitation evidence, and indicators.
- `correlation.py`: creates relationship records between events, CVEs, IOCs, actors, and malware.
- `deduplication.py`: exact and fuzzy duplicate detection using hashes and RapidFuzz.
- `enrichment.py`: AI provider abstraction and deterministic fallback enrichment.
- `scoring.py`: assigns LOW, MEDIUM, HIGH, or CRITICAL severity.
- `search.py`: MongoDB text search across intelligence collections.
- `source_config.py`: catalog and service for storing source plugin settings used by the frontend Settings page and collector runner.

## `frontend/`

Next.js web application for analysts.

- `package.json`: frontend dependencies and scripts.
- `next.config.ts`: Next.js config.
- `tsconfig.json`: TypeScript config.
- `tailwind.config.ts`: Tailwind theme and content config.
- `postcss.config.js`: PostCSS configuration for Tailwind.
- `app/layout.tsx`: root HTML layout and metadata.
- `app/page.tsx`: SOC dashboard screen.
- `app/globals.css`: global Tailwind imports and base page styles.

## `docker/`

Container build definitions.

- `Dockerfile.backend`: builds the Python backend image.
- `Dockerfile.frontend`: builds the Next.js frontend image.

## `infra/`

Local observability configuration.

- `prometheus.yml`: Prometheus scrape configuration for the API metrics endpoint.
- `grafana-dashboard.json`: starter Grafana dashboard definition.

## `scripts/`

Developer convenience scripts.

- `bootstrap.sh`: creates `.env`, creates a Python virtual environment, installs backend dev dependencies, and installs frontend dependencies.
- `run-api.sh`: starts the FastAPI API locally with reload enabled.

## `tests/`

Backend tests.

- `test_aggregation.py`: verifies duplicate event merging, confidence, scoring, and source preservation.
- `test_api.py`: verifies the API health endpoint.
- `test_deduplication.py`: verifies exact duplicate detection for matching CVEs and IOCs.
- `test_plugins.py`: verifies automatic plugin discovery.

## `docs/`

Human-facing project documentation.

- `Architecture.md`: explains the ingestion and processing architecture.
- `Deployment.md`: explains Docker Compose deployment.
- `API.md`: lists the API surface and authentication entrypoint.
- `Developer.md`: local development workflow.
- `Plugin-Development-Guide.md`: how to add new intelligence source plugins.
- `Repository-Guide.md`: this file.

## How Data Moves Through The Project

1. `apps/collectors/runner.py` asks `PluginRegistry` for all plugins.
2. Each plugin collects raw source data and normalizes it into `ThreatEvent`.
3. `AggregationService` merges related events.
4. `DeduplicationService` prevents repeated intelligence.
5. `ConfidenceService` calculates confidence.
6. `ThreatScoringService` assigns severity.
7. `CorrelationService` creates graph relationships.
8. `EnrichmentService` adds analyst-ready structured context.
9. `AlertService` decides alert routing.
10. `DiscordPublisher` posts or updates enriched alerts in Discord.
11. `apps/api/` exposes the stored intelligence to users and the frontend.

## Where To Start As A New Developer

Start with these files in this order:

1. `README.md`
2. `docs/Repository-Guide.md`
3. `core/models/domain.py`
4. `core/interfaces/plugin.py`
5. `apps/collectors/registry.py`
6. `apps/collectors/runner.py`
7. `core/services/aggregation.py`
8. `apps/api/main.py`
9. `frontend/app/page.tsx`

That path teaches you the domain model, plugin contract, ingestion flow, backend API, and frontend shell without forcing you to read every file at once.
