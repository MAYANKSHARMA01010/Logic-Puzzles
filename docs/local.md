# Local Setup Guide

Detailed local setup for Forecast-Audit.

## Prerequisites

- Python 3.11+
- Terminal access
- Port `7860` available

## Setup

1. Verify Python.

```bash
python --version
python3 --version
```

1. Enter the project directory.

```bash
cd Forecast-Audit
```

1. Create a virtual environment.

```bash
python -m venv .venv
```

1. Activate the environment.

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

1. Install dependencies.

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

1. Validate local environment.

```bash
python validate.py
```

1. Start the server.

```bash
python -m server.app
```

1. Run a health check from another terminal.

```bash
curl http://localhost:7860/health
```

Expected response:

```json
{"status":"healthy"}
```

## Local URLs

- Swagger UI: `http://localhost:7860/docs`
- ReDoc: `http://localhost:7860/redoc`
- OpenAPI schema: `http://localhost:7860/openapi.json`

For cross-mode URL details, see [Access URLs and Ports](./access-urls-and-ports.md).

## Useful Commands

Run baseline inference:

```bash
python inference.py
```

Run task distribution check:

```bash
python -c "from collections import Counter; from server.environment import TASKS; print(len(TASKS), Counter(t.difficulty for t in TASKS))"
```

Stop the server:

```text
Ctrl+C
```

Deactivate the virtual environment:

```bash
deactivate
```

## Troubleshooting

Port is already in use:

```bash
lsof -i :7860
kill -9 <PID>
```

Module import issues:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

More help: [Troubleshooting](./troubleshooting.md)
