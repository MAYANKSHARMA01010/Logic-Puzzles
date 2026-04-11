# Environment Variables

This page explains the environment variables used by Forecast-Audit, what they do, where they are used, and how to set them up.

## Why these variables exist

The project uses environment variables so secrets stay out of the codebase and the same app can run in local, Docker, GitHub Actions, and Hugging Face Spaces.

## Quick Setup

1. Copy the example file:

```bash
cp .env.example .env
```

1. Open `.env` and fill in your real values.

1. Keep placeholders in `.env.example` only.

## Variables

| Variable | Required | What it is for | Where it is used |
| --- | ---: | --- | --- |
| `HF_TOKEN` | Yes | Hugging Face token for validation and Space-related workflows | `scripts/validate-submission.sh`, `scripts/setup_env.sh`, `openenv.yaml` |
| `API_BASE_URL` | Yes | Base URL for the OpenAI-compatible API router | `scripts/setup_env.sh`, `openenv.yaml`, `inference.py` |
| `MODEL_NAME` | Yes | Model name used by the baseline runner | `scripts/setup_env.sh`, `openenv.yaml`, `inference.py` |
| `OPENAI_API_KEY` | Optional | API key used when you want `inference.py` to call an OpenAI-compatible model directly | `.env`, `inference.py` |
| `OPENAI_BASE_URL` | Optional | Base URL for the OpenAI-compatible client used by `inference.py` | `.env`, `inference.py` |
| `IMAGE_NAME` | Optional | Docker image tag used by helper scripts | `scripts/setup_env.sh`, Docker-related workflows |
| `TEMPERATURE` | Optional | Controls how random the model output is | `inference.py` |
| `MAX_TOKENS` | Optional | Controls output length from the model | `inference.py` |

## Minimal Recommended `.env`

```bash
HF_TOKEN=hf_xxxxx
API_BASE_URL=https://router.huggingface.co/v1
MODEL_NAME=Qwen/Qwen2.5-72B-Instruct
OPENAI_API_KEY=
OPENAI_BASE_URL=
IMAGE_NAME=forecast-audit-openenv:latest
TEMPERATURE=0.0
MAX_TOKENS=220
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
