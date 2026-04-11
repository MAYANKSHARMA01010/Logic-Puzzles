#!/usr/bin/env bash
set -euo pipefail

# Build the environment image from project root.
docker build -t forecast-audit-openenv:latest .

echo "Docker image built: forecast-audit-openenv:latest"
