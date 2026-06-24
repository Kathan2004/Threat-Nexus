# Developer Guide

Bootstrap locally:

```bash
./scripts/bootstrap.sh
```

Run backend checks:

```bash
ruff check .
mypy core apps
pytest
```

Run the API:

```bash
./scripts/run-api.sh
```

The codebase uses Pydantic models for domain contracts, repository classes for persistence, and explicit services for business behavior.
