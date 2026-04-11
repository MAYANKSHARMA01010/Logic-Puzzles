# Troubleshooting

This guide covers the most common local, Docker, and deployment issues.

## Quick Diagnostics

Run these first:

```bash
python validate.py
python inference.py
bash scripts/validate-submission.sh
openenv validate
```

If any command fails, use the sections below.

## Local Runtime Issues

### Port 7860 already in use

```bash
lsof -i :7860
kill -9 <PID>
```

Then restart:

```bash
python -m server.app
```

### Virtual environment not active

```bash
source .venv/bin/activate
python --version
```

### Dependency install failures

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Import errors

```bash
python -c "from server.app import app; print('ok')"
```

## Docker Issues

### Docker daemon not running

Start Docker Desktop (macOS/Windows) or Docker service (Linux), then retry.

### Container exits immediately

```bash
docker logs forecast-audit
```

Rebuild image:

```bash
docker build --no-cache -t forecast-audit-openenv .
```

### Cannot reach API from host

```bash
docker ps
```

Ensure port mapping includes `7860->7860`.

Test endpoint:

```bash
curl http://127.0.0.1:7860/health
```

## OpenEnv and Hugging Face Issues

### openenv CLI not found

```bash
pip install openenv-core
```

### HF token missing or invalid

Set token in `.env`:

```dotenv
HF_TOKEN=hf_xxxxx
```

Export environment:

```bash
source scripts/setup_env.sh
```

### Push fails due auth

```bash
openenv whoami
openenv push --repo-id Manku69/Forecast-Audit-OpenEnv
```

### Space runs older commit

Sync both remotes and push:

```bash
git fetch origin main
git fetch hf main
git push hf main
```

Verify SHAs:

```bash
git rev-parse --short origin/main
git rev-parse --short hf/main
```

## API Behavior Issues

### `/reset` returns 400

Likely invalid `task_id` or `difficulty`.

Valid difficulty values:

- `easy`
- `medium`
- `hard`

### `/step` returns 422

Action JSON is missing required fields or has invalid enum values.

Inspect schema:

```bash
curl http://127.0.0.1:7860/schema
```

### Inference script crashes

Use latest `inference.py` and ensure fallback behavior is intact.

Quick check:

```bash
python inference.py
```

## Still Blocked

Collect these and share them:

- failing command
- full error output
- output of `python --version`
- output of `pip list | head`
- output of `git status --short --branch`
