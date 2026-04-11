---
title: Forecast Audit OpenEnv
emoji: 📈
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# Forecast-Audit

Forecast-Audit is an OpenEnv-compatible benchmark environment for forecast and time-series quality auditing.

The agent acts like a data/forecast analyst and must:
- identify data quality issues
- repair missing or corrupted values
- respect business/operational constraints
- return structured actions with clear rationale

## What This Project Uses

- Python 3.11+
- FastAPI + Uvicorn for HTTP API serving
- Pydantic for request/response/state models
- OpenEnv spec (`openenv.yaml`) for environment packaging and validation
- Docker for containerized local and deployment runs
- Validation and inference scripts for local checks and baseline runs

## What This Project Does

- Provides task episodes through `POST /reset`
- Accepts agent decisions through `POST /step`
- Tracks environment state through `GET /state`
- Returns reward breakdowns to score action quality
- Supports easy, medium, and hard task difficulty paths
- Exposes a health endpoint for deployment checks

## Installation

See the dedicated setup pages:

- [docs/installation.md](docs/installation.md)
- [docs/quick-start.md](docs/quick-start.md)
- [docs/environment-variables.md](docs/environment-variables.md)

## Run Locally

Use [docs/local.md](docs/local.md) for full local run steps.

## Docker

Use [docs/docker.md](docs/docker.md) for Docker build and run steps.

## API Endpoints

- `POST /reset` -> starts a task episode
- `POST /step` -> submits one action
- `GET /state` -> returns current environment state
- `GET /health` -> health check

## Round 1 Quick Checks

Use [docs/round1/submission-guide.md](docs/round1/submission-guide.md) for Round 1 validation and submission checks.

## Project Structure

```text
Forecast-Audit/
├── server/
│   ├── app.py
│   └── environment.py
├── client.py
├── inference.py
├── models.py
├── openenv.yaml
├── requirements.txt
├── validate.py
└── scripts/
```

## Documentation Index

All detailed documentation is in separate Markdown files linked below.

- [Project Overview](docs/overview.md)
- [Quick Start in 5 Minutes](docs/quick-start.md)
- [Complete Installation Guide](docs/installation.md)
- [Environment Variables Guide](docs/environment-variables.md)
- [Run Locally (Detailed)](docs/local.md)
- [Run with Docker](docs/docker.md)
- [API Reference](docs/api-reference.md)
- [Task Format and Specs](docs/task-format.md)
- [System Architecture](docs/architecture.md)
- [Troubleshooting Guide](docs/troubleshooting.md)
- [Frequently Asked Questions](docs/faq.md)
- [Glossary of Terms](docs/glossary.md)
- [Contributing Guide](docs/contributing.md)
- [Round 1 Submission Guide](docs/round1/submission-guide.md)