# 🐳 Docker Setup Guide

Complete guide for running with Docker.

For a single reference of Local/Docker/HF URLs and port mapping, see [Access URLs and Ports](./access-urls-and-ports.md).

## Prerequisites

- Docker installed ([Download](https://www.docker.com/products/docker-desktop))
- Docker Desktop running (macOS/Windows)
- ~2GB disk space
- Port 7860 available

---

## Quick Start

```bash
cd Forecast-Audit
docker build -t forecast-audit-openenv .
docker run --rm -p 7860:7860 forecast-audit-openenv
```

Then visit: `http://localhost:7860/docs`

---

## Detailed Steps

### 1. Install Docker

**macOS/Windows:**
- Download Docker Desktop: https://www.docker.com/products/docker-desktop
- Install and launch

**Linux:**
```bash
sudo apt-get install docker.io
sudo systemctl start docker
```

**Verify Installation:**
```bash
docker --version
docker run hello-world
```

### 2. Navigate Project

```bash
cd Forecast-Audit
ls Dockerfile  # Verify Dockerfile exists
```

### 3. Build Image

```bash
docker build -t forecast-audit-openenv .
```

**Watch for:**
```
Step 1/5 : FROM python:3.11-slim
Step 2/5 : WORKDIR /app
Step 3/5 : COPY requirements.txt .
Step 4/5 : RUN pip install --no-cache-dir -r requirements.txt
Step 5/5 : COPY . .
Successfully tagged forecast-audit-openenv:latest
```

**Time:** ~5 minutes (first time), <1 minute (after cache)

### 4. Run Container

```bash
docker run --rm -p 7860:7860 forecast-audit-openenv
```

**Expected:**
```
INFO:     Started server process [1]
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:7860
```

### 5. Open in Browser

```
http://localhost:7860/docs
```

### 5b. Verify API From Host

Open a second terminal and run:

```bash
curl http://127.0.0.1:7860/health
curl -X POST http://127.0.0.1:7860/reset -H "Content-Type: application/json" -d '{"difficulty":"easy"}'
curl -X POST http://127.0.0.1:7860/reset -H "Content-Type: application/json" -d '{"difficulty":"medium"}'
curl -X POST http://127.0.0.1:7860/reset -H "Content-Type: application/json" -d '{"difficulty":"hard"}'
```

Expected: `/health` returns `{"status":"healthy"}` and each `/reset` returns a valid observation for the requested difficulty.

### 6. Stop Container

```bash
CTRL+C  # in terminal
```

---

## 🔧 Docker Commands

### Build Image

```bash
docker build -t forecast-audit-openenv .
```

### List Images

```bash
docker images
```

### Run Container

```bash
docker run --rm -p 7860:7860 forecast-audit-openenv
```

### Run in Background

```bash
docker run -d --name audit-env -p 7860:7860 forecast-audit-openenv
```

### View Logs

```bash
docker logs audit-env
docker logs -f audit-env  # Follow logs
```

### Stop Container

```bash
docker stop audit-env
```

### Remove Container

```bash
docker rm audit-env
```

### Interactive Shell

```bash
docker run -it forecast-audit-openenv /bin/bash
```

### Check Resource Usage

```bash
docker stats
```

---

## 🔗 Port Mapping

### Default (7860→7860)

```bash
docker run -p 7860:7860 forecast-audit-openenv
```

Visit: `http://localhost:7860`

### Custom Port (8000→7860)

```bash
docker run -p 8000:7860 forecast-audit-openenv
```

Visit: `http://localhost:8000`

---

## 📦 Image Management

### Save Image

```bash
docker save forecast-audit-openenv > audit-env.tar
```

### Load Image

```bash
docker load < audit-env.tar
```

### Remove Image

```bash
docker rmi forecast-audit-openenv
```

### Tag Image

```bash
docker tag forecast-audit-openenv myregistry/forecast-audit-openenv:v1.0
```

### Push to Registry

```bash
docker push myregistry/forecast-audit-openenv:v1.0
```

---

## ☁️ Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  forecast-audit:
    build: .
    ports:
      - "7860:7860"
    environment:
      - LOG_LEVEL=INFO
    restart: unless-stopped
```

Run:
```bash
docker-compose up
```

---

## 🔐 Best Practices

### Don't Run as Root

Add to Dockerfile:
```dockerfile
RUN useradd -m appuser
USER appuser
```

### Use Minimal Images

Already using `python:3.11-slim` ✓

### Keep Secrets Out

```bash
# Don't build with secrets
docker build --build-arg API_KEY=... .

# Use environment variables instead
docker run -e API_KEY=value ...
```

### Health Checks

```bash
docker run \
  --health-cmd='curl -f http://localhost:7860/health' \
  --health-interval=10s \
  forecast-audit-openenv
```

---

## 🚀 Production Deployment

### Multi-Stage Build

Optimize image size:
```dockerfile
FROM python:3.11-slim as builder
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
```

### Use Production Server

```bash
gunicorn -w 4 -b 0.0.0.0:7860 server.app:app
```

### Add Load Balancer

```yaml
services:
  lb:
    image: nginx
    ports:
      - "80:80"
  app1:
    build: .
  app2:
    build: .
  app3:
    build: .
```

---

## 🔍 Troubleshooting

### "Image not found"
```bash
docker build -t forecast-audit-openenv .  # Build first
```

### "Port already in use"
```bash
docker run -p 8000:7860 forecast-audit-openenv  # Use different port
```

### "Container keeps exiting"
```bash
docker logs <container_id>  # Check error
```

### "Permission denied"
```bash
sudo docker build ...  # Add sudo on Linux
```

### "Can't connect from browser"
```bash
# Check if running
docker ps

# Check logs
docker logs <container_name>

# Try direct IP
docker inspect <container_name> | grep IPAddress
curl http://<IP>:7860/health
```

---

## 📊 Dockerfile Reference

Our Dockerfile:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-m", "uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
```

Breakdown:
- `FROM` - Base image
- `WORKDIR` - Working directory
- `COPY` - Copy files
- `RUN` - Execute commands
- `CMD` - Default command to run

---

## 📈 Performance

### Image Size
Current: ~300MB

Optimizations:
- Use `slim` base image ✓
- Use `--no-cache-dir` for pip ✓

### Container Startup
Time: ~2 seconds

---

## 📝 Next Steps

- [Round 1 Submission Guide](./round1/submission-guide.md)
- [Round 1 Submission Guide](./round1/submission-guide.md)
- [Troubleshooting](./troubleshooting.md)

---

**Docker Setup Complete!**
