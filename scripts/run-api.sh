#!/usr/bin/env bash
set -euo pipefail

# Loopback only for local development. Use docker compose for anything else.
uvicorn apps.api.main:app --host 127.0.0.1 --port 8000 --reload
