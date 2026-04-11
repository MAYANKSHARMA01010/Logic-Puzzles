# Access URLs and Ports

This page is the single source of truth for where to access the app in local, Docker, and Hugging Face (HF) modes.

## Default Port

- Server listens on container/app port `7860`.
- Local access is usually through `http://127.0.0.1:7860` (or `http://localhost:7860`).

## Access Matrix

| Mode | How you run | Base URL to use | Docs URL | Notes |
| --- | --- | --- | --- | --- |
| Local Python | `python -m server.app` | `http://127.0.0.1:7860` | `http://127.0.0.1:7860/docs` | Uses app default port 7860 |
| Docker (default map) | `docker run --rm -p 7860:7860 forecast-audit-openenv` | `http://127.0.0.1:7860` | `http://127.0.0.1:7860/docs` | Host 7860 -> container 7860 |
| Docker (custom host port) | `docker run --rm -p 8000:7860 forecast-audit-openenv` | `http://127.0.0.1:8000` | `http://127.0.0.1:8000/docs` | Host port is 8000, app port remains 7860 |
| Hugging Face Space | Space deployment URL | `https://manku69-forecast-audit-openenv.hf.space` | `https://manku69-forecast-audit-openenv.hf.space/docs` | Public endpoint, no local port mapping |

## Core Endpoints

Use these paths on top of the base URL for any mode:

- `GET /health`
- `POST /reset`
- `POST /step`
- `GET /state`
- `GET /metadata`
- `GET /schema`

## Quick Verification

### Local

```bash
python validate.py
python -m server.app
```

In another terminal:

```bash
BASE_URL="http://127.0.0.1:7860"
curl "$BASE_URL/health"
curl -X POST "$BASE_URL/reset" -H "Content-Type: application/json" -d '{"difficulty":"easy"}'
```

### Docker

```bash
docker build -t forecast-audit-openenv .
docker run --rm -p 7860:7860 forecast-audit-openenv
```

In another terminal:

```bash
BASE_URL="http://127.0.0.1:7860"
curl "$BASE_URL/health"
curl -X POST "$BASE_URL/reset" -H "Content-Type: application/json" -d '{"difficulty":"medium"}'
```

### Hugging Face

```bash
BASE_URL="https://manku69-forecast-audit-openenv.hf.space"
curl "$BASE_URL/health"
curl -X POST "$BASE_URL/reset" -H "Content-Type: application/json" -d '{"difficulty":"hard"}'
```

## If Port 7860 Is Busy

- Find and stop conflicting process:

```bash
lsof -i :7860
kill -9 <PID>
```

- Or keep container/app on 7860 and change only host port in Docker:

```bash
docker run --rm -p 8000:7860 forecast-audit-openenv
```
