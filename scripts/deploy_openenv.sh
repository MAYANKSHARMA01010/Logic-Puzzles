#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ID="${1:-${OPENENV_REPO_ID:-Manku69/Forecast-Audit-OpenEnv}}"

if [[ -z "$REPO_ID" ]]; then
  echo "Usage: bash scripts/deploy_openenv.sh <username/repo-name>"
  echo "Or set OPENENV_REPO_ID in your shell or .env."
  exit 1
fi

cd "$REPO_DIR"

if [[ -f ".venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

if ! command -v openenv >/dev/null 2>&1; then
  echo "openenv CLI not found. Install it first (e.g. pip install openenv-core)."
  exit 1
fi

if [[ -f ".env" ]]; then
  # shellcheck disable=SC1091
  source scripts/setup_env.sh
else
  echo "Warning: .env not found. Continuing without setup_env exports."
fi

if [[ -z "${HF_TOKEN:-}" || "${HF_TOKEN}" == "hf_xxxxx" ]]; then
  echo "HF_TOKEN is missing or still set to placeholder value."
  echo "Update .env with a valid Hugging Face token, then rerun:"
  echo "  bash scripts/deploy_openenv.sh ${REPO_ID}"
  exit 1
fi

echo "[deploy] Validating environment..."
openenv validate

echo "[deploy] Pushing to $REPO_ID ..."
openenv push --repo-id "$REPO_ID"

echo "[deploy] Done."
