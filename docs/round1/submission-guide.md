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
4. Wait for the build
5. Test the live Space URL with `/reset`

## Baseline run

```bash
source scripts/setup_env.sh
.venv/bin/python inference.py
```

The script should print `[START]`, `[STEP]`, and `[END]` logs.
