#!/bin/bash
# COPY-PASTE COMMANDS FOR ROUND 1 SUBMISSION

cat << 'EOF'

╔════════════════════════════════════════════════════════════════════╗
║         PATTERN-PUZZLE-ENV — ROUND 1 SUBMISSION GUIDE             ║
║                     (Copy-Paste Commands)                         ║
╚════════════════════════════════════════════════════════════════════╝

🎯 GOAL: Get your environment validated and deployed to HF Spaces

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1: LOCAL SETUP (First time only)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 1a. Navigate to project
cd ~/Desktop/Projects/Logic-Puzzles

# 1b. Activate environment
source .venv/bin/activate

# 1c. Install dependencies (if not done)
pip install -r requirements.txt

# 1d. Setup .env file
cp .env.example .env
nano .env  # Add your HF_TOKEN here

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 2: VALIDATE BEFORE SUBMISSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Make script executable
chmod +x scripts/validate-submission.sh

# Run validation (must pass all 8 checks)
./scripts/validate-submission.sh

👆 MUST SHOW: ✅ All checks passed! Ready for Round 1.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 3: TEST LOCALLY (Before deploying)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Terminal 1: Start server
source scripts/setup_env.sh
.venv/bin/python -m uvicorn server.app:app --host 0.0.0.0 --port 7860

👆 Should show: INFO:     Uvicorn running on http://0.0.0.0:7860

# Terminal 2: Run baseline inference
source scripts/setup_env.sh
.venv/bin/python inference.py

👆 Should show structured logs:
   [START] task=sequence_guess...
   [STEP] step=1 action=... reward=... done=...
   [END] success=... steps=... score=... rewards=...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 4: BUILD DOCKER IMAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Build image (takes ~2-3 min, does not run)
docker build -t pattern-puzzle-env:latest -f server/Dockerfile .

# Test image locally (optional)
docker run -p 7860:7860 pattern-puzzle-env:latest

👆 Should start: INFO:     Uvicorn running on http://0.0.0.0:7860

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 5: DEPLOY TO HUGGING FACE SPACES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 5a. Create new Space
Go to: https://huggingface.co/new-space
  Name: pattern-puzzle-env
  SDK: Docker
  Visibility: Public
  → Click "Create Space"

# 5b. Clone the space repo
git clone https://huggingface.co/spaces/<your-username>/pattern-puzzle-env
cd pattern-puzzle-env

# 5c. Copy your code into space
cd ~/Desktop/Projects/Logic-Puzzles
git init
git add .
git commit -m "Initial OpenEnv submission for Round 1"
git remote add origin https://huggingface.co/spaces/<your-username>/pattern-puzzle-env
git push -u origin main

👆 HF Spaces auto-builds. Wait 5-10 minutes for deployment.

# 5d. Test your space
SPACE_URL="https://<your-username>-pattern-puzzle-env.hf.space"
curl -X POST "$SPACE_URL/reset" -H "Content-Type: application/json" -d '{}'

👆 Should return 200 OK with observation data

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 6: SUBMIT TO ROUND 1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Go to Round 1 submission portal and submit:
# - Space URL: https://<your-username>-pattern-puzzle-env.hf.space
# - Repo: https://huggingface.co/spaces/<your-username>/pattern-puzzle-env
# - Problem statement: [select one from round details]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ CHECKLIST BEFORE SUBMITTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

☑️  ./scripts/validate-submission.sh passes (8/8 checks)
☑️  .venv/bin/python inference.py runs without errors
☑️  docker build succeeds
☑️  openenv validate passes
☑️  HF Space is live and responds to /reset
☑️  .env has HF_TOKEN, API_BASE_URL, MODEL_NAME
☑️  README.md has Installation section
☑️  inference.py uses correct log format: [START], [STEP], [END]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ COMMON ISSUES & FIXES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Issue: "openenv validate" fails
→ Fix: openenv.yaml syntax error. Check YAML indentation

Issue: Docker build fails
→ Fix: Missing dependencies in Dockerfile. Add: openai, httpx

Issue: inference.py can't connect to server
→ Fix: Start server first in separate terminal (see STEP 3)

Issue: HF Space shows "Error" badge
→ Fix: Check Space logs. Usually Docker image issue.
  Go to Space Settings → View logs

Issue: "HF_TOKEN error 403"
→ Fix: Token doesn't have Inference API permission
  Get new token from: https://huggingface.co/settings/tokens

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📞 NEED HELP?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

See detailed guide: cat SUBMISSION_GUIDE.md
Quick validation:  ./scripts/validate-submission.sh
OpenEnv docs:      https://github.com/openenv-framework/openenv

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Ready? Start with: ./scripts/validate-submission.sh

EOF
