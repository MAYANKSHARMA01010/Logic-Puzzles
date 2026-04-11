#!/usr/bin/env bash
set -euo pipefail

source .env

 : "${API_BASE_URL:=https://router.huggingface.co/v1}"
 : "${MODEL_NAME:=Qwen/Qwen2.5-72B-Instruct}"
 : "${IMAGE_NAME:=forecast-audit-openenv:latest}"

export HF_TOKEN
export API_BASE_URL
export MODEL_NAME
export IMAGE_NAME

echo "Environment variables exported for this shell session."
echo "Tip: run 'source scripts/setup_env.sh' to keep them in your current terminal."
