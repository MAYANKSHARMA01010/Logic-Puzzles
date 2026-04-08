# Local Run

Use two terminals.

## Terminal 1: start the server

```bash
source scripts/setup_env.sh
.venv/bin/python -m uvicorn server.app:app --host 0.0.0.0 --port 7860 --reload
```

## Terminal 2: run the agent

```bash
source scripts/setup_env.sh
.venv/bin/python inference.py
```

## Quick health check

```bash
curl -X POST http://localhost:7860/reset -H "Content-Type: application/json" -d '{}'
```
