#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$REPO_DIR/.env"

if [[ ! -f "$ENV_FILE" ]]; then
  echo ".env not found at $ENV_FILE"
  echo "Create it with: cp .env.example .env"
  return 1 2>/dev/null || exit 1
fi

# Export variables from .env into the current shell when sourced.
set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a

: "${API_BASE_URL:=https://router.huggingface.co/v1}"
: "${MODEL_NAME:=Qwen/Qwen2.5-72B-Instruct}"
: "${IMAGE_NAME:=forecast-audit-openenv:latest}"

export HF_TOKEN
export API_BASE_URL
export MODEL_NAME
export IMAGE_NAME

echo "Environment variables exported for this shell session."
echo "Tip: run 'source scripts/setup_env.sh' to keep them in your current terminal."
