# API

The FastAPI service exposes OpenAPI at `/docs`.

Primary resources:

- `GET /events`
- `POST /events`
- `GET /alerts`
- `GET /cves`
- `GET /actors`
- `GET /campaigns`
- `GET /malware`
- `GET /iocs`
- `GET /correlations`
- `GET /search?q=term`
- `GET /dashboard`
- `GET /analytics`

Authenticated endpoints expect a bearer token from `POST /auth/token`.
