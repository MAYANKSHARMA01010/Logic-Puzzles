#!/usr/bin/env bash
set -euo pipefail

# Build the environment image from project root.
docker build -t my-pattern-env:latest -f server/Dockerfile .

echo "Docker image built: my-pattern-env:latest"
