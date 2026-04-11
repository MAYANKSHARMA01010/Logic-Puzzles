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

Quick local verification:

```bash
python validate.py
python inference.py
python -c "from collections import Counter; from server.environment import TASKS; print(len(TASKS), Counter(t.difficulty for t in TASKS))"
```

Expected: validation passes, inference prints summary JSON, and task counts show 33 total with 11 each for easy/medium/hard.

## Docker

Use [docs/docker.md](docs/docker.md) for Docker build and run steps.

Quick Docker verification:

```bash
docker build -t forecast-audit-openenv .
docker run --rm -p 7860:7860 forecast-audit-openenv
```

In another terminal:

```bash
curl http://127.0.0.1:7860/health
curl -X POST http://127.0.0.1:7860/reset -H "Content-Type: application/json" -d '{"difficulty":"easy"}'
curl -X POST http://127.0.0.1:7860/reset -H "Content-Type: application/json" -d '{"difficulty":"medium"}'
curl -X POST http://127.0.0.1:7860/reset -H "Content-Type: application/json" -d '{"difficulty":"hard"}'
```

## Hugging Face Space

- Space page: https://huggingface.co/spaces/Manku69/Forecast-Audit-OpenEnv
- Live app URL: https://manku69-forecast-audit-openenv.hf.space

Quick live tests:

```bash
SPACE_URL="https://manku69-forecast-audit-openenv.hf.space"

curl "$SPACE_URL/health"

curl -X POST "$SPACE_URL/reset" \
	-H "Content-Type: application/json" \
	-d '{"difficulty":"easy"}'

curl -X POST "$SPACE_URL/step" \
	-H "Content-Type: application/json" \
	-d '{
		"operation": "impute",
		"target_index": 3,
		"predicted_value": 135.0,
		"severity": "low",
		"violated_constraints": [],
		"rationale": "Stable +5 ramp"
	}'

curl "$SPACE_URL/state"
```

Expected: `/health` returns `{"status":"healthy"}`, and `/reset` and `/step` return valid JSON payloads.

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