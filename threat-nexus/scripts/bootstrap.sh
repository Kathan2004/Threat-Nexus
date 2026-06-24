#!/usr/bin/env bash
set -euo pipefail

cp -n .env.example .env
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
cd frontend
npm install
