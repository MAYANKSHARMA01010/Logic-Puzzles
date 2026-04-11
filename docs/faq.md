# FAQ

## What is Forecast-Audit?

Forecast-Audit is an OpenEnv-compatible environment for evaluating agent actions on time-series quality issues such as missing values, anomalies, and invalid forecasts.

## How do I run it locally?

Use the quick flow:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m server.app
```

Then open `http://localhost:7860/docs`.

## How do I validate my setup?

Run:

```bash
python validate.py
python inference.py
bash scripts/validate-submission.sh
```

## How do I run it with Docker?

```bash
docker build -t forecast-audit-openenv .
docker run --rm -p 7860:7860 forecast-audit-openenv
```

## Which endpoints are available?

- `GET /health`
- `POST /reset`
- `POST /step`
- `GET /state`
- `GET /metadata`
- `GET /schema`

## Why does my submission say inference failed?

Most common causes:

- unhandled exception in `inference.py`
- missing or invalid API credentials
- malformed model JSON response

Use the current hardened `inference.py`, then rerun local checks.

## Why does Hugging Face Space look one commit behind?

Your `hf` remote may not be synced with `origin`.

```bash
git fetch origin main
git fetch hf main
git push hf main
```

## Where are all setup docs?

Start with:

- [Quick Start](./quick-start.md)
- [Installation](./installation.md)
- [Local Setup](./local.md)
- [Docker Guide](./docker.md)
- [Troubleshooting](./troubleshooting.md)
