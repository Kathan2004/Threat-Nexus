# Deployment

Copy `.env.example` to `.env`, set secrets, and start the stack:

```bash
docker compose up --build
```

Services:

- API: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3001`

Production deployments should replace the example JWT secret, use managed MongoDB and Redis, configure Discord credentials, and put the API behind TLS-aware ingress with request logging enabled.
