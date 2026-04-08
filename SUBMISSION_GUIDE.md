# ROUND 1 SUBMISSION GUIDE

This guide will get your environment ready for OpenEnv Round 1 submission.

## ✅ Pre-Submission Checklist

Run this before submitting:

```bash
chmod +x scripts/validate-submission.sh
./scripts/validate-submission.sh
```

Expected output:
```
========================================
✓ Passed: 8 checks
✅ All checks passed! Ready for Round 1.
```

---

## 📋 What Gets Evaluated

| Criteria | Weight | Status |
|----------|--------|--------|
| Real-world utility | 30% | ✅ Pattern recognition is real AI task |
| Task & grader quality | 25% | ✅ 25 tasks, 3 tiers, reproducible graders |
| Environment design | 20% | ✅ Clean OpenEnv spec, proper rewards |
| Code quality & spec compliance | 15% | ✅ Types, openenv.yaml, Dockerfile |
| Creativity & novelty | 10% | ✅ Interesting reward shaping, first-try bonuses |

---

## 🚀 Local Testing (Before Submission)

### 1. Validate Everything Works

```bash
# Terminal 1: Start server
source scripts/setup_env.sh
.venv/bin/python -m uvicorn server.app:app --host 0.0.0.0 --port 7860

# Terminal 2: Run baseline (should complete in < 1 min)
source scripts/setup_env.sh
.venv/bin/python inference.py
```

Expected output:
```
[START] task=sequence_guess env=my_pattern_env model=Qwen/Qwen2.5-72B-Instruct
[STEP] step=1 action=10 reward=0.50 done=false error=null
[STEP] step=2 action=15 reward=2.00 done=true error=null
[END] success=true steps=2 score=0.571 rewards=0.50,2.00
```

### 2. Docker Build Test

```bash
docker build -t pattern-puzzle-env:latest -f server/Dockerfile .
docker run -p 7860:7860 pattern-puzzle-env:latest
```

Should see:
```
INFO:     Uvicorn running on http://0.0.0.0:7860
INFO:     Application startup complete
```

### 3. OpenEnv Spec Validation

```bash
openenv validate
```

Should pass silently or show success.

---

## 📦 Environment Details (For Judges)

### Real-World Utility
- **Domain:** Sequence pattern recognition (used in IQ tests, standardized exams, AI evaluation)
- **Tasks:** 25 curated puzzles ranging from simple arithmetic to complex sequences (look-and-say, triangular numbers, factorials)
- **Grading:** Exact match with numeric normalization (handles "6.25" vs "6.250")
- **Agent Interaction:** Standard HTTP/REST, compatible with any LLM

### Task Tiers

**Easy (8 tasks) - max 3 attempts:**
- Simple arithmetic: 2,4,6,8,? → 10
- Fibonacci: 1,1,2,3,5,? → 8
- Base reward: 1.0

**Medium (10 tasks) - max 3 attempts:**
- Multiplication: 3,9,27,81,? → 243
- Letter patterns: A,C,E,G,? → I
- Alternating: 2,6,7,21,22,? → 66
- Base reward: 2.0

**Hard (7 tasks) - max 2 attempts:**
- Factorials: 1,2,6,24,120,? → 720
- Primes: 2,3,5,7,11,? → 13
- Look-and-say: 1,11,21,1211,111221,? → 312211
- Base reward: 3.0

### Scoring Formula

```
reward = base_by_difficulty + efficiency_bonus
efficiency_bonus = (remaining_attempts / max_attempts)
max_possible_score = 3.0 (hard task) + 1.0 (first try) = 4.0
normalized_score = sum_rewards / 3.5 (clamped to [0.0, 1.0])
```

---

## 🔄 How to Deploy to HF Spaces

1. **Create new Space on Hugging Face:**
   - Go to https://huggingface.co/new-space
   - Choose "Docker" as the Space SDK
   - Name: `pattern-puzzle-env`
   - Visibility: Public

2. **Push your code:**
   ```bash
   git init
   git add .
   git commit -m "Initial submission"
   git remote add origin https://huggingface.co/spaces/<your-username>/pattern-puzzle-env
   git push -u origin main
   ```
   HF will auto-build & deploy

3. **Verify Space is live:**
   ```bash
   curl -X POST https://<your-username>-pattern-puzzle-env.hf.space/health
   # Should return: {"status": "ok"}
   ```

---

## ⚡ Key Commands

| Task | Command |
|------|---------|
| **Local test** | `.venv/bin/python inference.py` |
| **Validate submission** | `./scripts/validate-submission.sh` |
| **Check spec** | `openenv validate` |
| **Build Docker** | `docker build -f server/Dockerfile .` |
| **Start server** | `.venv/bin/python -m uvicorn server.app:app --host 0.0.0.0 --port 7860` |

---

## 📝 Files Required for Submission

✅ `openenv.yaml` — Environment specification  
✅ `server/Dockerfile` — Container config  
✅ `inference.py` — Baseline script  
✅ `validate.py` — Local validation  
✅ `requirements.txt` — Dependencies  
✅ `README.md` — Documentation  
✅ `.env.example` — Config template  
✅ `scripts/validate-submission.sh` — Submission checker  

---

## 🎯 Success Criteria

Your submission passes if:

- ✅ HF Space deploys and pings `/reset` with 200 OK
- ✅ `openenv validate` passes  
- ✅ `docker build` succeeds  
- ✅ `inference.py` runs without errors
- ✅ 25+ tasks with graders (✓ checkmark if tasks work)
- ✅ Graders return scores in [0.0, 1.0]
- ✅ Structured logs: `[START]`, `[STEP]`, `[END]`

---

## ⚠️ Common Mistakes (Avoid These)

❌ Hardcoded HF_TOKEN (always use .env)  
❌ Graders that return same score always (needs variance)  
❌ Missing `inference.py` in root  
❌ Dockerfile that doesn't expose 7860  
❌ Inconsistent log format (breaks automated scoring)  
❌ Runtime > 20 minutes per episode  

---

## 🚢 Ready to Submit?

1. Run validation: `./scripts/validate-submission.sh`
2. Test locally: `.venv/bin/python inference.py`
3. Create HF Space
4. Push code to Space
5. Wait for deployment (2-5 min)
6. Submit link to Round 1 portal

**Questions?** See the provided problem statement.

Good luck! 🎯
