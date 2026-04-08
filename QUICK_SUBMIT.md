# ⚡ QUICK START: ROUND 1 SUBMISSION (Copy-Paste Only)

```bash
# 1️⃣ Navigate and activate
cd ~/Desktop/Projects/Logic-Puzzles
source .venv/bin/activate

# 2️⃣ Setup .env (one time)
cp .env.example .env
# Open .env and add your HF_TOKEN from https://huggingface.co/settings/tokens

# 3️⃣ Validate everything works
chmod +x scripts/validate-submission.sh
./scripts/validate-submission.sh

# Expected: ✅ All checks passed! Ready for Round 1.

# 4️⃣ Test locally (Terminal 1)
source scripts/setup_env.sh
.venv/bin/python -m uvicorn server.app:app --host 0.0.0.0 --port 7860

# 5️⃣ Test locally (Terminal 2, separate)
source scripts/setup_env.sh
.venv/bin/python inference.py

# Expected output:
# [START] task=sequence_guess env=my_pattern_env model=Qwen/Qwen2.5-72B-Instruct
# [STEP] step=1 action=10 reward=0.50 done=false error=null
# [STEP] step=2 action=15 reward=2.00 done=true error=null
# [END] success=true steps=2 score=0.571 rewards=0.50,2.00

# 6️⃣ Build Docker
docker build -t pattern-puzzle-env:latest -f server/Dockerfile .

# 7️⃣ Create HF Space (one time)
# Go to: https://huggingface.co/new-space
# - SDK: Docker
# - Name: pattern-puzzle-env
# - Visibility: Public

# 8️⃣ Deploy to HF Space
git init
git add .
git commit -m "OpenEnv Round 1 submission"
git remote add origin https://huggingface.co/spaces/<YOUR-USERNAME>/pattern-puzzle-env
git push -u origin main

# Wait 5-10 minutes for HF to build and deploy

# 9️⃣ Verify Space is live
SPACE_URL="https://<YOUR-USERNAME>-pattern-puzzle-env.hf.space"
curl -X POST "$SPACE_URL/reset" -H "Content-Type: application/json" -d '{}'

# Expected: 200 OK response with observation data

# 🔟 Submit to Round 1
# Go to Round 1 portal and submit:
# - Space URL: https://<YOUR-USERNAME>-pattern-puzzle-env.hf.space
# - Repo: https://huggingface.co/spaces/<YOUR-USERNAME>/pattern-puzzle-env

```

---

## Files Created for Round 1:

✅ `openenv.yaml` — Environment specification  
✅ `scripts/validate-submission.sh` — Validation script  
✅ `SUBMISSION_GUIDE.md` — Detailed guide  
✅ `ROUND1_STEPS.sh` — Step-by-step instructions  
✅ `QUICK_SUBMIT.md` — This file (quick reference)  

---

## Project Stats (For Judges):

📊 **Difficulty Tiers:**
- Easy: 8 tasks, 3 attempts each, base reward 1.0
- Medium: 10 tasks, 3 attempts each, base reward 2.0
- Hard: 7 tasks, 2 attempts each, base reward 3.0

📊 **Scoring:**
- Max possible: 3.5 (hard task on first try)
- Efficiency bonus: Remaining attempts / max attempts
- Normalized: [0.0 to 1.0]

📊 **Real-world utility:**
- Pattern recognition (used in IQ tests, AI evaluation benchmarks)
- HTTP REST interface (any LLM can play)
- Reproducible graders with exact answer matching

---

## Files to Submit:

Submit your HF Space URL to the Round 1 portal. Everything is contained in the Space repo.

Required files (auto-checked):
- `openenv.yaml` ✓
- `server/Dockerfile` ✓
- `inference.py` ✓
- `requirements.txt` ✓
- `README.md` ✓
- `.env.example` ✓

---

## Still have questions?

```bash
# View full guide
cat SUBMISSION_GUIDE.md

# View all copy-paste steps
bash ROUND1_STEPS.sh

# Quick validation
./scripts/validate-submission.sh
```

**Good luck! 🚀**
