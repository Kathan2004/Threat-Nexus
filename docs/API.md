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

Authenticated endpoints expect a bearer token from `POST /auth/token` (`{"username": "...", "password": "..."}`).

| Method | Path | Role | Purpose |
|---|---|---|---|
| POST | `/auth/token` | public, 10/min | exchange credentials for a JWT |
| GET | `/auth/me` | any | current principal |
| GET | `/auth/users` | admin | list accounts |
| POST | `/auth/users` | admin | create an account (`password` 12-72 chars) |
