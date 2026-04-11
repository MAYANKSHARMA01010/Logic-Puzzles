#!/usr/bin/env bash
set -euo pipefail

# Quick commands for local setup and submission
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$REPO_DIR"

if [[ -f ".venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

if [[ ! -f ".env" ]]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

chmod +x scripts/validate-submission.sh
./scripts/validate-submission.sh
