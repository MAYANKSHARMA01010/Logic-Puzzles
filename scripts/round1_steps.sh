#!/bin/bash
# Copy-paste commands for Round 1

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$REPO_DIR"
source .venv/bin/activate
cp .env.example .env
pip install -r requirements.txt
python validate.py
