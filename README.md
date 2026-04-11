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

- [docs/clone.md](docs/clone.md)
- [docs/local-run.md](docs/local-run.md)
- [docs/docker-run.md](docs/docker-run.md)

## Run Locally

Use [docs/local-run.md](docs/local-run.md) for full local run steps.

## Docker

Use [docs/docker-run.md](docs/docker-run.md) for Docker build and run steps.

## API Endpoints

- `POST /reset` -> starts a task episode
- `POST /step` -> submits one action
- `GET /state` -> returns current environment state
- `GET /health` -> health check

## Round 1 Quick Checks

Use [docs/round1-checks.md](docs/round1-checks.md) for Round 1 validation and submission checks.

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

- [docs/index.md](docs/index.md)
- [docs/clone.md](docs/clone.md)
- [docs/local-run.md](docs/local-run.md)
- [docs/docker-run.md](docs/docker-run.md)
- [docs/round1-checks.md](docs/round1-checks.md)
- [docs/overview.md](docs/overview.md)
- [docs/quick-start.md](docs/quick-start.md)
- [docs/installation.md](docs/installation.md)
- [docs/local.md](docs/local.md)
- [docs/docker.md](docs/docker.md)
- [docs/api-reference.md](docs/api-reference.md)
- [docs/task-format.md](docs/task-format.md)
- [docs/architecture.md](docs/architecture.md)
- [docs/troubleshooting.md](docs/troubleshooting.md)
- [docs/faq.md](docs/faq.md)
- [docs/glossary.md](docs/glossary.md)
- [docs/contributing.md](docs/contributing.md)
- [docs/round1/checklist.md](docs/round1/checklist.md)
- [docs/round1/quick-submit.md](docs/round1/quick-submit.md)
- [docs/round1/submission-guide.md](docs/round1/submission-guide.md)