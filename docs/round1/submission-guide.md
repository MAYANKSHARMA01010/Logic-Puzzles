# Round 1 Submission Guide

## Before you submit

Run the validator first:

```bash
chmod +x scripts/validate-submission.sh
./scripts/validate-submission.sh
```

Recommended local preflight:

```bash
python validate.py
python inference.py
```

## What the judges check

- The Space responds to `POST /reset`
- `openenv.yaml` exists and matches the environment
- Docker builds successfully
- `inference.py` runs without errors
- The task set has easy, medium, and hard forecasting-audit tasks

## Deploy steps

1. Create a Hugging Face Space
2. Choose Docker
3. Validate locally: `openenv validate`
4. Deploy with OpenEnv CLI: `openenv push --repo-id <username>/<space-name>`
5. Add required Secrets (`HF_TOKEN`, `API_BASE_URL`, `MODEL_NAME`, and `IMAGE_NAME` if needed)
6. Wait for the build
7. Test the live Space URL with `/reset` and `/step`

### OpenEnv Deploy Command

```bash
source .venv/bin/activate
source scripts/setup_env.sh

# Validate before deploy
openenv validate

# Deploy to HF Space
openenv push --repo-id your-username/forecast-audit-openenv

# Optional: private space
openenv push --repo-id your-username/forecast-audit-openenv --private
```

If you prefer a reusable wrapper:

```bash
bash scripts/deploy_openenv.sh your-username/forecast-audit-openenv
```

### Current Space

- Space page: [https://huggingface.co/spaces/Manku69/Forecast-Audit-OpenEnv](https://huggingface.co/spaces/Manku69/Forecast-Audit-OpenEnv)
- Live URL: [https://manku69-forecast-audit-openenv.hf.space](https://manku69-forecast-audit-openenv.hf.space)

### Live API smoke tests

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

Expected responses:

- `GET /health` returns `{"status":"healthy"}`
- `POST /reset` returns JSON with `observation` and `done`
- `POST /step` returns JSON with `observation`, `reward`, `done`, and `info`
- `GET /state` returns current state JSON

## Baseline run

```bash
source scripts/setup_env.sh
.venv/bin/python inference.py
```

The script prints a JSON summary including `task_scores` and `average_score`.

For complete URL/port mapping and verification commands across Local, Docker, and HF, see [Access URLs and Ports](../access-urls-and-ports.md).
