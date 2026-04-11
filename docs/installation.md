# 📚 Complete Installation Guide

Complete step-by-step installation instructions for all scenarios.

## 🎯 Choose Your Path

- **[🏃 Quick Start](#quick-installation)** (5 minutes) - Just run it!
- **[🔧 Detailed Local](#detailed-local-installation)** (15 minutes) - Full explanation
- **[🐳 Docker](#docker-installation)** (10 minutes) - Container setup
- **[☁️ Cloud](#cloud-deployment)** (30 minutes) - AWS/GCP/Azure

---

## ⚡ Quick Installation

### Prerequisites
- Python 3.11+
- Terminal/Command line
- ~200MB disk space

### Commands
```bash
cd /Users/mayanksharma/Desktop/Projects/forecast-audit-env
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python validate.py
python -m server.app
```

Visit: `http://localhost:7860/docs`

✅ **Done in 5 minutes!**

---

## 🔧 Detailed Local Installation

### Step 1: Check Python

```bash
python --version
python3 --version
```

**Need Python?**
- **macOS**: `brew install python@3.11`
- **Ubuntu**: `sudo apt-get install python3.11`
- **Windows**: https://www.python.org/downloads/

### Step 2: Navigate to Project

```bash
cd /Users/mayanksharma/Desktop/Projects/forecast-audit-env
pwd  # Shows current directory
ls -la  # Lists files
```

Expected files:
```
requirements.txt
server/
models.py
README.md
Dockerfile
```

### Step 3: Create Virtual Environment

```bash
# Create venv
python -m venv .venv

# Activate (macOS/Linux)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Verify activation (should see (.venv) prefix)
which python  # should show .venv/bin/python
```

### Step 4: Upgrade pip

```bash
pip install --upgrade pip setuptools wheel
pip --version
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

Expected packages:
```
✓ fastapi
✓ uvicorn
✓ pydantic
✓ openai
✓ httpx
✓ pyyaml
✓ openenv-core
```

### Step 6: Verify Installation

```bash
python validate.py
```

Expected output:
```
✓ reset() and state() are consistent
✓ reward range stays within [0.0, 1.0]
✓ grading is deterministic
✓ hard task allows multi-step interaction

All local validation checks passed.
```

### Step 7: Start Server

```bash
python -m server.app
```

Expected output:
```
INFO:     Started server process [8785]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:7860 (Press CTRL+C to quit)
```

### Step 8: Open in Browser

```
http://localhost:7860/docs
```

✅ **Installation Complete!**

---

## 🐳 Docker Installation

### Prerequisites
- Docker installed ([Installation Guide](https://docs.docker.com/get-docker/))
- Docker Desktop running (macOS/Windows)
- ~1GB disk space

### Step 1: Navigate to Project

```bash
cd /Users/mayanksharma/Desktop/Projects/forecast-audit-env
```

### Step 2: Build Image

```bash
docker build -t forecast-audit-openenv .
```

**Watch for:**
- `Step 1/5` through `Step 5/5`
- Final: `Successfully tagged forecast-audit-openenv:latest`
- Time: ~5 minutes (first time)

### Step 3: Run Container

```bash
docker run --rm -p 7860:7860 forecast-audit-openenv
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:7860
```

### Step 4: Open in Browser

```
http://localhost:7860/docs
```

### Step 5: Stop Container

```bash
CTRL+C  # in terminal
```

✅ **Docker Setup Complete!**

---

## ☁️ Cloud Deployment

### AWS Elastic Container Service (ECS)

#### Step 1: Push Image to ECR

```bash
# Login to AWS
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Tag image
docker tag forecast-audit-openenv:latest \
  123456789012.dkr.ecr.us-east-1.amazonaws.com/forecast-audit-openenv:latest

# Push
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/forecast-audit-openenv:latest
```

#### Step 2: Create ECS Task Definition

```json
{
  "family": "forecast-audit-env",
  "containerDefinitions": [
    {
      "name": "forecast-audit-env",
      "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/forecast-audit-openenv:latest",
      "portMappings": [
        {
          "containerPort": 7860,
          "hostPort": 7860,
          "protocol": "tcp"
        }
      ]
    }
  ]
}
```

#### Step 3: Create ECS Service

```bash
aws ecs create-service \
  --cluster my-cluster \
  --service-name forecast-audit \
  --task-definition forecast-audit-env:1 \
  --desired-count 1
```

---

### Google Cloud Run

```bash
# Build
gcloud builds submit --tag gcr.io/PROJECT_ID/forecast-audit-openenv

# Deploy
gcloud run deploy forecast-audit-openenv \
  --image gcr.io/PROJECT_ID/forecast-audit-openenv \
  --platform managed \
  --region us-central1 \
  --port 7860
```

---

### Azure Container Instances

```bash
az container create \
  --resource-group myResourceGroup \
  --name forecast-audit-env \
  --image forecast-audit-openenv:latest \
  --ports 7860 \
  --ip-address Public
```

---

## ✅ Verification Checklist

### Local Installation
- [ ] Python 3.11+ installed
- [ ] Virtual environment created
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] `validate.py` passes all checks
- [ ] Server starts without errors
- [ ] Browser opens `/docs` page

### Docker Installation
- [ ] Docker installed and running
- [ ] Image builds successfully
- [ ] Container starts without errors
- [ ] Port 7860 is accessible
- [ ] Browser opens `/docs` page

### API Endpoints
- [ ] GET `/health` returns 200
- [ ] GET `/metadata` returns task list
- [ ] POST `/reset` initializes task
- [ ] POST `/step` accepts actions
- [ ] GET `/state` returns current state

---

## 🔄 Re-installation / Fresh Start

### Complete Reset

```bash
# Deactivate venv
deactivate

# Remove venv
rm -rf .venv

# Recreate
python -m venv .venv

# Activate
source .venv/bin/activate

# Install
pip install -r requirements.txt

# Validate
python validate.py
```

---

## 🚫 Common Installation Issues

### Issue: "command not found: python3"
**Solution**: Install Python 3.11+

### Issue: "ModuleNotFoundError: No module named 'fastapi'"
**Solution**: 
```bash
source .venv/bin/activate  # Activate venv
pip install -r requirements.txt  # Reinstall
```

### Issue: "Permission denied" on Linux/macOS
**Solution**:
```bash
chmod +x .venv/bin/python
```

### Issue: Docker: "image not found"
**Solution**:
```bash
docker build -t forecast-audit-openenv .  # Build first
docker run -p 7860:7860 forecast-audit-openenv
```

---

## 📋 Installation Summary

| Method | Time | Difficulty | Best For |
|--------|------|------------|----------|
| Local | 5min | Easy | Development |
| Docker | 10min | Medium | Consistency |
| Cloud | 30min | Hard | Production |

---

**Installation Complete!** Next: [Quick Start](./quick-start.md)
