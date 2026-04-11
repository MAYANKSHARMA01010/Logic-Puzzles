# 💾 Local Setup Guide

Detailed guide for running on your local machine.

## Prerequisites

- Python 3.11+
- macOS, Linux, or Windows
- Terminal/Command line access
- ~200MB disk space
- Port 7860 available

---

## Setup Steps

### 1. Verify Python

```bash
python --version
python3 --version
which python3
```

Should show 3.11 or higher.

### 2. Navigate Project

```bash
cd /Users/mayanksharma/Desktop/Projects/Forecast-Audit
cat requirements.txt  # Verify files exist
```

### 3. Create Virtual Environment

```bash
python -m venv .venv
```

Creates isolated Python environment.

### 4. Activate Virtual Environment

**macOS/Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

**Verify:** You should see `(.venv)` prefix in terminal.

### 5. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Watch for:
```
Successfully installed fastapi-0.115.0 uvicorn ...
```

### 6. Validate Installation

```bash
python validate.py
```

Expected: All checks pass ✓

### 7. Start Server

```bash
python -m server.app
```

Expected:
```
INFO:     Started server process [8785]
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:7860
```

### 8. Test API

In new terminal:
```bash
curl http://localhost:7860/health
```

Should return:
```json
{"status":"healthy"}
```

---

## 🌐 Access Server

### Swagger UI (Interactive)
```
http://localhost:7860/docs
```

### ReDoc (Documentation)
```
http://localhost:7860/redoc
```

### OpenAPI Schema
```
http://localhost:7860/openapi.json
```

---

## 🛠️ Development Workflow

### Enable Hot Reload

```bash
uvicorn server.app:app --host 0.0.0.0 --port 7860 --reload
```

Now changes auto-reload without restarting.

### Run Tests

```bash
python validate.py  # Validation checks
python inference.py  # Baseline scoring
```

### Debug Mode

```bash
DEBUG=1 python -m server.app
```

Or:
```bash
python -c "from server.app import app; app"
```

---

## 📊 Project Structure

```
Forecast-Audit/
├── server/                 # Core server code
│   ├── app.py             # FastAPI application
│   └── environment.py      # Main logic
├── models.py              # Data models
├── client.py              # HTTP client
├── inference.py           # Baseline tests
├── validate.py            # Validation
├── requirements.txt       # Dependencies
└── .venv/                # Virtual environment (local)
```

---

## 🔧 Common Commands

### Start Server
```bash
python -m server.app
```

### Test API
```bash
curl http://localhost:7860/health
```

### Run Validation
```bash
python validate.py
```

### Stop Server
```bash
CTRL+C  # in terminal
```

### Deactivate venv
```bash
deactivate
```

### Check Installed Packages
```bash
pip list
```

### Check Requirements
```bash
pip freeze > requirements.txt
```

---

## 🐛 Debugging

### Check Python Path

```bash
python -c "import sys; print(sys.path)"
```

### Check Module Imports

```bash
python -c "from server.app import app; print('Success')"
```

### View Server Logs

```bash
python -m server.app 2>&1 | tee server.log
```

Save logs to file.

### Test Individual Components

```bash
# Test models
python -c "from models import ForecastAuditAction; print('OK')"

# Test environment
python -c "from server.environment import ForecastAuditEnvironment; print('OK')"
```

---

## 🆘 Troubleshooting

### Port Already in Use

```bash
lsof -i :7860
kill -9 <PID>
```

### Module Not Found

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Python Not Found

```bash
which python3
/usr/local/bin/python3 -m server.app
```

---

## 📈 Performance

### Monitor Resource Usage

```bash
# CPU & Memory
top

# Or specific to Python
ps aux | grep python
```

### Typical Performance

- Startup: < 2 seconds
- Health check: < 10ms
- Reset task: < 100ms
- Step action: < 50ms
- Memory: ~50MB idle

---

## 🔐 Local Development Tips

### Keep Secrets Safe

Don't commit:
```bash
.venv/
__pycache__/
*.pyc
.env  # If you add one
```

### Use .gitignore

```bash
cat .gitignore
```

### Tag Commits

```bash
git tag -a v1.0 -m "Version 1.0"
git push origin v1.0
```

---

## 📝 Next Steps

- [API Reference](./api-reference.md)
- [Task Format](./task-format.md)
- [Architecture Deep Dive](./architecture.md)

---

**Local Setup Complete!**
