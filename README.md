# Logic-Puzzles

An AI pattern puzzle game where an agent learns to solve sequences and earn points based on difficulty and speed.

## Installation & Setup (Copy-Paste Commands)

### **Step 1: Clone and Navigate**
```bash
cd /path/to/where/you/want/project
# If cloning from repo:
git clone <repo-url> Logic-Puzzles
cd Logic-Puzzles
```

### **Step 2: Create Virtual Environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### **Step 3: Get HuggingFace API Token**
1. Go to https://huggingface.co/settings/tokens
2. Click "Create new token"
3. Select "Fine-grained token"
4. Name it: `pattern-puzzle-demo`
5. Check "Make calls to Inference Providers" ✓
6. Copy the token

### **Step 4: Setup Environment File**
```bash
cp .env.example .env
nano .env  # Or use your editor
```

Paste your token in `.env`:
```
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
API_BASE_URL=https://router.huggingface.co/v1
MODEL_NAME=Qwen/Qwen2.5-72B-Instruct
IMAGE_NAME=my-pattern-env:latest
```

Save and exit (Ctrl+X, then Y, then Enter if using nano)

### **Step 5: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 6: Validate Everything Works**
```bash
python validate.py
```

Expected output:
```
==================================================
✅ ALL CHECKS PASSED - READY FOR JUDGES
==================================================
```

---

## Quick Start (After Setup Above)

### **Run Locally - Terminal 1 (Server)**
```bash
source scripts/setup_env.sh
.venv/bin/python -m uvicorn server.app:app --host 0.0.0.0 --port 7860 --reload
```

Expected:
```
INFO:     Uvicorn running on http://0.0.0.0:7860
INFO:     Application startup complete
```

### **Run Locally - Terminal 2 (AI Agent)**
```bash
source scripts/setup_env.sh
.venv/bin/python inference.py
```

Expected:
```
[START] task=sequence_guess env=my_pattern_env model=Qwen/Qwen2.5-72B-Instruct
[STEP] step=1 action=10 reward=0.50 done=false error=null
[STEP] step=2 action=15 reward=2.00 done=true error=null
[END] success=true steps=2 score=0.571 rewards=0.50,2.00
```

### **Run in Docker**
```bash
source scripts/setup_env.sh
bash scripts/build_image.sh
.venv/bin/python inference.py  # Uses from_docker_image() to start container
```

## Project Structure

- `server/environment.py` — Game logic (25 puzzles, 3 difficulty tiers, reward calculation)
- `server/app.py` — FastAPI server with `/reset` and `/step` endpoints
- `client.py` — HTTP client for agent to communicate with server
- `inference.py` — AI agent that connects to LLM (Qwen via HF) and plays the game
- `models.py` — Pydantic data contracts
- `validate.py` — Pre-submission validation script

## Scoring

- **Easy tasks:** 1.0 base points + efficiency bonus (0-1.0)
- **Medium tasks:** 2.0 base points + efficiency bonus (0-1.0)
- **Hard tasks:** 3.0 base points + efficiency bonus (0-1.0)
- **Max episode score:** 3.5 (hard task solved on first try)

## API Endpoints

- `POST /reset` — Start new episode
- `POST /step` — Submit guess
- `GET /state` — Debug: view game state
- `GET /health` — Health check