# Installation Guide

This page covers installation for local Python and Docker workflows.

## Quick Install

```bash
git clone https://github.com/MAYANKSHARMA01010/Forecast-Audit
cd Forecast-Audit
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Then run:

```bash
python validate.py
```

## Local Python Installation

### Requirements

- Python 3.11+
- `pip`
- Terminal access

### Steps

1. Create and activate virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
```

1. Install dependencies.

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

1. Configure environment values.

```bash
cp .env.example .env
```

1. Update `.env` values as needed:

- `HF_TOKEN`
- `API_BASE_URL`
- `MODEL_NAME`

1. Validate setup.

```bash
python validate.py
python inference.py
```

## Docker Installation

### Docker Requirements

- Docker Desktop (macOS/Windows) or Docker Engine (Linux)

### Build

```bash
docker build -t forecast-audit-openenv .
```

### Run

```bash
docker run --rm -p 7860:7860 forecast-audit-openenv
```

### Verify

```bash
curl http://127.0.0.1:7860/health
curl -X POST http://127.0.0.1:7860/reset -H "Content-Type: application/json" -d '{"difficulty":"easy"}'
```

## OpenEnv CLI Setup

Install OpenEnv CLI:

```bash
pip install openenv-core
```

Validate project:

```bash
openenv validate
```

Deploy to Hugging Face Space:

```bash
openenv push --repo-id Manku69/Forecast-Audit-OpenEnv
```

## Validation Checklist

```bash
python validate.py
python inference.py
bash scripts/validate-submission.sh
openenv validate
```

## Related Docs

- [Quick Start](./quick-start.md)
- [Local Setup](./local.md)
- [Docker Guide](./docker.md)
- [Environment Variables](./environment-variables.md)
- [Round 1 Submission Guide](./round1/submission-guide.md)
