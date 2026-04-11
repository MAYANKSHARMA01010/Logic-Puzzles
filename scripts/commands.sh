#!/bin/bash
# Quick commands for local setup and submission

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$REPO_DIR"
source .venv/bin/activate
cp .env.example .env
chmod +x scripts/validate-submission.sh
./scripts/validate-submission.sh
