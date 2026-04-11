# 🔧 Troubleshooting Guide

Solutions for common issues and problems.

## 🚨 Common Issues

### 1. Port 7860 Already in Use

**Error:**
```
ERROR: [Errno 48] error while attempting to bind on address ('0.0.0.0', 7860)
```

**Cause:** Another process is using port 7860

**Solution:**

```bash
# Find what's using port 7860
lsof -i :7860

# Kill the process
kill -9 <PID>

# Or run on a different local port
uvicorn server.app:app --host 0.0.0.0 --port 8000

# For Docker, remap host port instead
docker run --rm -p 8000:7860 forecast-audit-openenv
```

See [Access URLs and Ports](./access-urls-and-ports.md) for the full run-mode matrix.

---

### 2. Python Not Found / Command Not Found

**Error:**
```
command not found: python
zsh: command not found: python3
```

**Cause:** Python not in PATH or not installed

**Solution:**

```bash
# Check if Python is installed
which python3

# Install Python (macOS)
brew install python@3.11

# Use full path to Python
/usr/local/bin/python3 --version

# Or use from venv
source .venv/bin/activate
```

---

### 3. Virtual Environment Not Activated

**Error:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Cause:** Dependencies not installed or venv not activated

**Solution:**

```bash
# Activate venv
source .venv/bin/activate

# You should see (.venv) prefix in terminal

# Then install
pip install -r requirements.txt
```

---

### 4. Package Installation Failed

**Error:**
```
ERROR: Could not find a version that satisfies the requirement fastapi>=0.115.0
```

**Cause:** Pip cache corrupted or network issue

**Solution:**

```bash
# Clear pip cache
pip cache purge

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Try install again
pip install -r requirements.txt

# Or use specific Python version
python3.11 -m pip install -r requirements.txt
```

---

### 5. ImportError / ModuleNotFoundError

**Error:**
```
ImportError: No module named 'server'
ModuleNotFoundError: No module named 'models'
```

**Cause:** Not in correct directory or Python path issue

**Solution:**

```bash
# Make sure you're in project root
cd Forecast-Audit
pwd  # Should show Forecast-Audit

# Try running from project root
python -m server.app

# Or check Python path
python -c "import sys; print(sys.path)"
```

---

### 6. Server Starts But No Response

**Error:**
```
Starting server but curl gets no response
```

**Cause:** Server not fully started or firewall blocking

**Solution:**

```bash
# Wait a bit longer for startup
sleep 3

# Test connection
curl http://localhost:7860/health

# Check if process is actually running
ps aux | grep "python -m server"

# Try with explicit localhost
curl http://127.0.0.1:7860/health

# Check firewall
sudo lsof -i :7860
```

---

### 7. Docker: Image Build Failed

**Error:**
```
docker build failed: "No such file or directory"
```

**Cause:** Wrong directory or Dockerfile not found

**Solution:**

```bash
# Navigate to project root
cd Forecast-Audit

# Check Dockerfile exists
ls -la Dockerfile

# Try build with explicit path
docker build -t forecast-audit-openenv .

# Check for syntax errors in Dockerfile
cat Dockerfile
```

---

### 8. Docker: Container Won't Start

**Error:**
```
docker: Error response from daemon
```

**Cause:** Port already in use or resource issues

**Solution:**

```bash
# Check running containers
docker ps -a

# Stop conflicting container
docker stop <container_id>

# Remove stopped containers
docker container prune

# Try with different port
docker run -p 8000:7860 forecast-audit-openenv

# Check resources
docker stats  # View CPU/Memory usage
```

---

### 9. API Returns 422 Validation Error

**Error:**
```json
{
  "detail": [
    {"loc": ["body", "operation"], "msg": "field required"}
  ]
}
```

**Cause:** Missing required field or wrong data type

**Solution:**

```bash
# Check request body format
curl -X POST http://localhost:7860/step \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "impute",
    "target_index": 3,
    "predicted_value": 135.0,
    "severity": "low",
    "violated_constraints": [],
    "rationale": "explanation"
  }'

# Verify all required fields are present
# operation (required)
# target_index (optional)
# predicted_value (optional)
# severity (optional)
# violated_constraints (required)
# rationale (required)
```

---

### 10. API Returns 400 Bad Request

**Error:**
```json
{
  "detail": "Invalid task_id or difficulty"
}
```

**Cause:** Wrong task_id or difficulty value

**Solution:**

```bash
# Get valid task IDs
curl http://localhost:7860/metadata

# Use valid task from response
# Valid difficulty: easy, medium, hard

# Example correct request
curl -X POST http://localhost:7860/reset \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "easy_ops_missing_001",
    "difficulty": "easy"
  }'
```

---

## 📊 Validation Checklist

Before running, verify:

### Setup
- [ ] Python 3.11+ installed
- [ ] Project folder accessible
- [ ] Port 7860 is free
- [ ] ~500MB disk space available

### Local Run
- [ ] Virtual environment created
- [ ] Virtual environment activated (`(.venv)` prefix visible)
- [ ] Dependencies installed
- [ ] `python validate.py` passes all checks
- [ ] Server starts without errors

### Docker Run
- [ ] Docker installed and running
- [ ] Docker Desktop app is open (macOS)
- [ ] 2GB free disk space
- [ ] Port 7860 is free
- [ ] Dockerfile exists

### API Testing
- [ ] Server responds to `curl http://localhost:7860/health`
- [ ] Browser opens `http://localhost:7860/docs`
- [ ] Swagger UI loads
- [ ] `/reset` endpoint responds
- [ ] `/step` endpoint accepts valid actions

---

## 🔍 Debug Mode

### Enable Verbose Logging

```bash
# Show detailed server logs
LOGLEVEL=DEBUG python -m server.app

# Show curl verbose output
curl -v http://localhost:7860/health

# Python debugging
python -c "import server.app; print(server.app.__file__)"
```

### Test Individual Components

```bash
# Test models
python -c "from models import ForecastAuditAction; print('Models OK')"

# Test environment
python -c "from server.environment import ForecastAuditEnvironment; print('Environment OK')"

# Test imports
python -c "import fastapi; print(fastapi.__version__)"
```

---

## 🆘 Getting Help

### Step 1: Check This Guide
Does your error match any above? → Follow solution

### Step 2: Check Project Issues
Visit GitHub issues → Search error message

### Step 3: Check FAQ
See [FAQ.md](./faq.md)

### Step 4: Check Logs
```bash
# Save server output to file
python -m server.app > server.log 2>&1

# View logs
cat server.log
```

### Step 5: Create Minimal Example
Reproduce error in simplest form:
```python
import requests
r = requests.get('http://localhost:7860/health')
print(r.status_code)
print(r.json())
```

### Step 6: Open Issue
Include:
- Error message (full)
- Environment (Python version, OS)
- Steps to reproduce
- Logs/screenshots

---

## 💡 Pro Tips

### Kill Process on Port
```bash
# macOS/Linux
lsof -i :7860 | grep -v COMMAND | awk '{print $2}' | xargs kill -9

# Find stuck Python processes
ps aux | grep python | grep -v grep
```

### Reset Everything
```bash
# Complete clean reset
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python validate.py
```

### Test with Different Tools

```bash
# Using Python requests
python << 'EOF'
import requests
r = requests.get('http://localhost:7860/health')
print(r.json())
EOF

# Using httpie (if installed)
http GET localhost:7860/health

# Using wget
wget -qO- http://localhost:7860/health
```

### Docker Debugging
```bash
# View Docker logs
docker logs <container_id>

# Interactive shell in container
docker exec -it <container_id> /bin/bash

# Check environment in container
docker run -it forecast-audit-openenv env
```

---

**Troubleshooting Guide Complete** ✅

Still stuck? Check [FAQ.md](./faq.md) or open an issue!
