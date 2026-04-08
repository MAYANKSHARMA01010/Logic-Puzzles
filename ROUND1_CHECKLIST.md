# ROUND 1 SUBMISSION: COMPLETE CHECKLIST

## 📦 What You Have (Pattern-Puzzle-Env)

A containerized OpenEnv environment where AI agents solve pattern puzzles.

### Skills Evaluated ✅

- **Real-world utility (30%)**: Pattern recognition benchmark (IQ test style)
- **Task quality (25%)**: 25 tasks, 3 difficulty tiers, accurate graders
- **Environment design (20%)**: Clean OpenEnv spec, proper rewards, episodes
- **Code quality (15%)**: Types, openenv.yaml, working Dockerfile
- **Creativity (10%)**: Smart reward bonuses, difficulty progression

---

## 🎯 Before Submitting (Required)

### Step 1: Local Validation
```bash
chmod +x scripts/validate-submission.sh
./scripts/validate-submission.sh
```
Must pass ALL 8 checks.

### Step 2: Test Locally
```bash
# Terminal 1
source scripts/setup_env.sh
.venv/bin/python -m uvicorn server.app:app --host 0.0.0.0 --port 7860

# Terminal 2
source scripts/setup_env.sh
.venv/bin/python inference.py
```
Must complete without errors, show structured logs.

### Step 3: Docker Build
```bash
docker build -t pattern-puzzle-env:latest -f server/Dockerfile .
```
Must succeed.

### Step 4: OpenEnv Validate
```bash
openenv validate
```
Must pass spec compliance.

---

## 📋 Files Ready for Judges

| File | Purpose | Status |
|------|---------|--------|
| `openenv.yaml` | "What is this environment?" | ✅ |
| `server/Dockerfile` | "How to containerize it?" | ✅ |
| `inference.py` | "Example agent plays it" | ✅ |
| `requirements.txt` | "What packages needed?" | ✅ |
| `README.md` | "How to use locally?" | ✅ |
| `.env.example` | "What config values?" | ✅ |
| `scripts/validate-submission.sh` | "Is it valid?" | ✅ |
| `SUBMISSION_GUIDE.md` | "Detailed submission guide" | ✅ |

---

## 🚀 Deployment Steps (HF Spaces)

### 1. Create Space
- Go to: https://huggingface.co/new-space
- SDK: **Docker**
- Name: **pattern-puzzle-env**
- Visibility: **Public**

### 2. Deploy Code
```bash
git init
git add .
git commit -m "OpenEnv Round 1 - Pattern Puzzle Environment"
git remote add origin https://huggingface.co/spaces/<YOUR-USERNAME>/pattern-puzzle-env
git push -u origin main
```

### 3. Wait for Build
- HF Spaces auto-builds from Dockerfile
- Takes 5-10 minutes
- Can check logs if needed

### 4. Verify Live
```bash
curl -X POST https://<YOUR-USERNAME>-pattern-puzzle-env.hf.space/reset \
  -H "Content-Type: application/json" -d '{}'
```
Should return 200 OK with observation data.

---

## ✅ Pre-Submission Verification

Run this final checklist:

```bash
# 1. All scripts pass
./scripts/validate-submission.sh

# 2. Inference runs
source scripts/setup_env.sh
timeout 120 .venv/bin/python inference.py

# 3. Docker builds
docker build -f server/Dockerfile . -t test:latest

# 4. OpenEnv valid
openenv validate

# 5. Files exist
ls -la openenv.yaml server/Dockerfile inference.py requirements.txt README.md
```

All must succeed. ✅ = Ready to submit.

---

## 📝 Submission Portal

When Round 1 opens:

**Submission URL:** https://your-space-url.hf.space  
**Example:** https://mayank-pattern-puzzle-env.hf.space

Go to Round 1 portal and submit this URL.

Judges will:
1. ✅ Ping your space (/reset endpoint)
2. ✅ Check openenv.yaml spec
3. ✅ Build Docker image
4. ✅ Run your inference.py
5. ✅ Evaluate quality on criteria above

---

## 🎯 Competition Scoring

| Category | Points | What Judges Look For |
|----------|--------|----------------------|
| Real-world Utility | 30 | Would people use this to train agents? |
| Task Quality | 25 | Graders accurate? Good difficulty curve? |
| Environment Design | 20 | Clean state? Good rewards? Good episodes? |
| Code Quality | 15 | Follows spec? Works? Documented? |
| Creativity | 10 | Cool mechanics? Novel domain? Clever reward? |
| **TOTAL** | **100** | **Your Final Score** |

---

## ⚠️ Disqualification (Don't Do These)

❌ Space doesn't ping  
❌ Grader returns same score always  
❌ Missing inference.py  
❌ Plagiarized code  
❌ Runtime > 20 minutes  

---

## 🎬 Ready?

1. Run validation:
   ```bash
   ./scripts/validate-submission.sh
   ```

2. If all pass, read:
   ```bash
   cat QUICK_SUBMIT.md
   ```

3. Follow HF Space deployment steps above

4. Submit URL to Round 1 portal

**Good luck! You've got this.** 🚀

---

**Need debugging help?**
```bash
# View full submission guide
cat SUBMISSION_GUIDE.md

# View quick steps
bash ROUND1_STEPS.sh

# Check what failed
./scripts/validate-submission.sh
```
