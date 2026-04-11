# ⚡ Quick Start (5 Minutes)

Get the Forecast Audit OpenEnv running in less than 5 minutes!

## 🏃 Local Setup (Recommended for First-Time)

### 1. Clone/Navigate to Project
```bash
cd /Users/mayanksharma/Desktop/Projects/forecast-audit-env
```

### 2. Create Python Environment
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Validate Setup
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

### 5. Start Server
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

### 6. Open in Browser
```
http://localhost:7860/docs
```

✅ **You're done! Interactive API docs are open.**

---

## 🐳 Docker Setup (1 Command)

### Build & Run
```bash
cd /Users/mayanksharma/Desktop/Projects/forecast-audit-env
docker build -t forecast-audit-openenv .
docker run --rm -p 7860:7860 forecast-audit-openenv
```

### Open in Browser
```
http://localhost:7860/docs
```

✅ **Done!**

---

## 🧪 Test the API

### Option A: Swagger UI (Easiest)
1. Open `http://localhost:7860/docs`
2. Click **POST /reset** → Click **Execute**
3. Click **POST /step** → Enter action → Click **Execute**
4. Click **GET /state** → Click **Execute**

### Option B: curl Commands

#### 1. Reset
```bash
curl -X POST http://localhost:7860/reset \
  -H "Content-Type: application/json" \
  -d '{"task_id": "easy_ops_missing_001"}'
```

#### 2. Step
```bash
curl -X POST http://localhost:7860/step \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "impute",
    "target_index": 3,
    "predicted_value": 135.0,
    "severity": "low",
    "violated_constraints": [],
    "rationale": "Stable ramp of +5 per hour"
  }'
```

#### 3. State
```bash
curl http://localhost:7860/state
```

---

## ✅ What's Working?

| Component | Status |
|-----------|--------|
| Server | ✅ Running on port 7860 |
| API Endpoints | ✅ All 3 routes working |
| Documentation | ✅ Swagger UI accessible |
| Validation | ✅ All checks passed |

---

## 🔥 Next Steps

Choose your path:

### 👶 I'm a Beginner
→ Read [Overview](./overview.md)

### 👨‍💻 I'm a Developer
→ Read [API Reference](./api-reference.md)

### 🐳 I'm DevOps
→ Read [Docker Setup](./docker.md)

### 🤖 I Want to Build an Agent
→ Read [Building an Agent](./tutorials/03-building-an-agent.md)

---

## ❌ Troubleshooting

### Port Already in Use
```bash
lsof -i :7860
kill -9 <PID>
```

### Python Not Found
Make sure you activated venv:
```bash
source .venv/bin/activate
```

### Package Installation Failed
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### More Issues?
See [Troubleshooting](./troubleshooting.md)

---

**You're ready to go! 🚀**
