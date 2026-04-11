# Environment Variables

This page explains the environment variables used by Forecast-Audit, what they do, where they are used, and how to set them up.

## Why these variables exist

The project uses environment variables so secrets stay out of the codebase and the same app can run in local, Docker, GitHub Actions, and Hugging Face Spaces.

## Quick Setup

1. Copy the example file:

```bash
cp .env.example .env
```

2. Open `.env` and fill in your real values.
3. Keep placeholders in `.env.example` only.

## Variables

| Variable | Required | What it is for | Where it is used |
|---|---:|---|---|
| `HF_TOKEN` | Yes | Hugging Face token for validation and Space-related workflows | `scripts/validate-submission.sh`, `scripts/setup_env.sh`, `openenv.yaml` |
| `API_BASE_URL` | Yes | Base URL for the OpenAI-compatible API router | `scripts/setup_env.sh`, `openenv.yaml`, `inference.py` |
| `MODEL_NAME` | Yes | Model name used by the baseline runner | `scripts/setup_env.sh`, `openenv.yaml`, `inference.py` |
| `OPENAI_API_KEY` | Optional | API key used when you want `inference.py` to call an OpenAI-compatible model directly | `.env`, `inference.py` |
| `OPENAI_BASE_URL` | Optional | Base URL for the OpenAI-compatible client used by `inference.py` | `.env`, `inference.py` |
| `IMAGE_NAME` | Optional | Docker image tag used by helper scripts | `scripts/setup_env.sh`, Docker-related workflows |
| `PATTERN_TASK` | Optional | Task label used by some helper commands or experiments | `.env` only unless you need it in your own tooling |
| `PATTERN_BENCHMARK` | Optional | Benchmark label used by helper commands or experiments | `.env` only unless you need it in your own tooling |
| `MAX_STEPS` | Optional | Limits how many steps the baseline runner or experiments should take | `.env` and any custom runner logic |
| `TEMPERATURE` | Optional | Controls how random the model output is | `inference.py` |
| `MAX_TOKENS` | Optional | Controls output length from the model | `inference.py` |
| `MAX_TOTAL_REWARD` | Optional | Used for custom scoring or reporting workflows | `.env` only unless you add custom scoring |
| `SUCCESS_SCORE_THRESHOLD` | Optional | Used for custom pass/fail reporting workflows | `.env` only unless you add custom scoring |

## Minimal Recommended `.env`

```bash
HF_TOKEN=hf_xxxxx
API_BASE_URL=https://router.huggingface.co/v1
MODEL_NAME=Qwen/Qwen2.5-72B-Instruct
OPENAI_API_KEY=
OPENAI_BASE_URL=
IMAGE_NAME=forecast-audit-openenv:latest
PATTERN_TASK=sequence_guess
PATTERN_BENCHMARK=my_pattern_env
MAX_STEPS=3
TEMPERATURE=0.3
MAX_TOKENS=50
MAX_TOTAL_REWARD=3.5
SUCCESS_SCORE_THRESHOLD=0.1
```

## Notes

- Put real secret values only in `.env`.
- Keep `.env.example` safe for sharing.
- If you only run the heuristic baseline, `OPENAI_API_KEY` can stay blank.
- If you use a Hugging Face router, set `API_BASE_URL` and `MODEL_NAME`.
- If you use the OpenAI-compatible baseline path, set `OPENAI_API_KEY` and `OPENAI_BASE_URL`.

## Related Files

- [.env.example](../.env.example)
- [openenv.yaml](../openenv.yaml)
- [scripts/setup_env.sh](../scripts/setup_env.sh)
- [scripts/validate-submission.sh](../scripts/validate-submission.sh)
- [inference.py](../inference.py)
