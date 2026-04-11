# Quick Start

Run Forecast-Audit locally in a few minutes.

For URL and port mappings across local, Docker, and Hugging Face, see [Access URLs and Ports](./access-urls-and-ports.md).

## Local Setup

1. Clone and enter the repository.

```bash
git clone https://github.com/MAYANKSHARMA01010/Forecast-Audit
cd Forecast-Audit
```

1. Create and activate a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
```

1. Install dependencies.

```bash
pip install -r requirements.txt
```

1. Run validation checks.

```bash
python validate.py
```

1. Start the API server.

```bash
python -m server.app
```

1. Open API docs.

```text
http://localhost:7860/docs
```

## Docker Setup

Build and run with Docker:

```bash
docker build -t forecast-audit-openenv .
docker run --rm -p 7860:7860 forecast-audit-openenv
```

Open API docs:

```text
http://localhost:7860/docs
```

## API Smoke Test

Reset a task:

```bash
curl -X POST http://localhost:7860/reset \
  -H "Content-Type: application/json" \
  -d '{"task_id":"easy_ops_missing_001"}'
```

Submit an action:

```bash
curl -X POST http://localhost:7860/step \
  -H "Content-Type: application/json" \
  -d '{
    "operation":"impute",
    "target_index":3,
    "predicted_value":135.0,
    "severity":"low",
    "violated_constraints":[],
    "rationale":"Stable +5 ramp"
  }'
```

Read state:

```bash
curl http://localhost:7860/state
```

## Next Steps

- Review the [API Reference](./api-reference.md)
- Review the [Task Format](./task-format.md)
- Follow [Round 1 Submission Guide](./round1/submission-guide.md)
- Use [Troubleshooting](./troubleshooting.md) if needed
