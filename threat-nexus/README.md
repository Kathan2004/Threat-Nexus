# Threat Nexus

Threat Nexus is a Cyber Threat Intelligence Platform for aggregating, normalizing, enriching, correlating, scoring, storing, searching, and distributing security intelligence.

## Repository Tree

```text
apps/              Service entrypoints and plugin implementations
core/              Shared domain models, repositories, interfaces, auth, and services
frontend/          Next.js SOC interface
docker/            Backend and frontend container builds
infra/             Prometheus and Grafana assets
tests/             Backend unit and API tests
docs/              Architecture, deployment, API, developer, and plugin guides
scripts/           Local developer commands
```

For a full file-by-file walkthrough, read [docs/Repository-Guide.md](docs/Repository-Guide.md).
For environment variables and source credentials, read [docs/Configuration.md](docs/Configuration.md).

## Roadmap

1. Harden authentication with persisted users and refresh tokens.
2. Add source-specific API clients and credential validation.
3. Persist collection runs and plugin metrics.
4. Expand graph APIs for visualization.
5. Add OpenTelemetry traces.
6. Add Discord thread synchronization workers.
7. Add frontend API integration and analyst workflows.

## Local Start

```bash
cp .env.example .env
docker compose up --build
```

Open the API at `http://localhost:8000/docs` and the frontend at `http://localhost:3000`.
