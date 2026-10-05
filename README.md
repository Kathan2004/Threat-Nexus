# Threat Nexus

Threat Nexus is a Cyber Threat Intelligence Platform for aggregating, normalizing, enriching, correlating, scoring, storing, searching, and distributing security intelligence.

```
 collectors (18 plugins) ──► normalize ──► dedupe ──► enrich (LLM / deterministic) ──► correlate ──► score
   CISA KEV, NVD, OTX, VT, Shodan, Censys, GreyNoise,                                         │
   AbuseIPDB, MISP, OpenCTI, IntelOwl, URLhaus,                 MongoDB ◄─────────────────────┘
   MalwareBazaar, ransomware.live, GitHub, Reddit, news            │
                                                     FastAPI (JWT + RBAC) ──► Next.js SOC UI
                                                                   └──► Discord distribution, Prometheus/Grafana
```

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

1. Add refresh tokens and password rotation endpoints.
2. Add source-specific API clients and credential validation.
3. Persist collection runs and plugin metrics.
4. Expand graph APIs for visualization.
5. Add OpenTelemetry traces.
6. Add Discord thread synchronization workers.
7. Add frontend API integration and analyst workflows.

## Local Start

```bash
cp .env.example .env
# Set at least: JWT_SECRET, ADMIN_USERNAME, ADMIN_PASSWORD, GRAFANA_ADMIN_PASSWORD
python -c "import secrets; print(secrets.token_urlsafe(48))"   # use for JWT_SECRET
docker compose up --build
```

The API docs are at `http://localhost:8000/docs` and the frontend at `http://localhost:3000`. Sign in with the admin account.
Every published port is bound to `127.0.0.1`; put a TLS reverse proxy in front for remote access.

## Security Model

- **Accounts.** Users are stored in MongoDB with bcrypt hashes. The first admin is created from `ADMIN_USERNAME` and `ADMIN_PASSWORD` when the users collection is empty. Admins manage accounts through `GET/POST /auth/users`.
- **Tokens.** `POST /auth/token` issues HS256 JWTs carrying the user's stored roles (`admin`, `analyst`, `viewer`, `service`). Login is rate limited to 10/minute per client.
- **JWT secret.** `JWT_SECRET` is mandatory outside development and must be at least 32 characters.
- **Network exposure.** MongoDB, Redis and Prometheus are not published to the host. Grafana requires an admin password and has sign-up disabled.
- **CI.** Runs ruff, mypy, pytest with coverage, a frontend build and a gitleaks secret scan.

Report vulnerabilities privately; see [SECURITY.md](SECURITY.md).

## Development

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
ruff check . && mypy core apps && pytest
cd frontend && npm ci && npm run dev
```
