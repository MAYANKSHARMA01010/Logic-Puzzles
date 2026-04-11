# Round 1 Submission Guide

## Before you submit

Run the validator first:

```bash
chmod +x scripts/validate-submission.sh
./scripts/validate-submission.sh
```

## What the judges check

- The Space responds to `POST /reset`
- `openenv.yaml` exists and matches the environment
- Docker builds successfully
- `inference.py` runs without errors
- The task set has easy, medium, and hard puzzles

## Deploy steps

1. Create a Hugging Face Space
2. Choose Docker
3. Push the repo
4. Add required Secrets (`HF_TOKEN`, `API_BASE_URL`, `MODEL_NAME`, and `IMAGE_NAME` if needed)
5. Wait for the build
6. Test the live Space URL with `/reset` and `/step`

### Current Space

- Space page: https://huggingface.co/spaces/Manku69/Forecast-Audit-OpenEnv
- Live URL: https://manku69-forecast-audit-openenv.hf.space

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

## Baseline run

```bash
source scripts/setup_env.sh
.venv/bin/python inference.py
```

The script should print `[START]`, `[STEP]`, and `[END]` logs.
