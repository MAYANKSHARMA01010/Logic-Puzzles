#!/bin/bash
# MINIMAL COPY-PASTE: Just run these commands in order

# PART 1: SETUP (one time)
cd ~/Desktop/Projects/Logic-Puzzles
source .venv/bin/activate
cp .env.example .env
# ⚠️ EDIT .env and add your HF_TOKEN from https://huggingface.co/settings/tokens

# PART 2: VALIDATE
chmod +x scripts/validate-submission.sh
./scripts/validate-submission.sh
# ✅ Should show: "All checks passed! Ready for Round 1"

# PART 3: TEST (two terminals)
# Terminal A:
source scripts/setup_env.sh
.venv/bin/python -m uvicorn server.app:app --host 0.0.0.0 --port 7860

# Terminal B:
source scripts/setup_env.sh
.venv/bin/python inference.py
# ✅ Should show structured logs with scores

# PART 4: DOCKER BUILD
docker build -t pattern-puzzle-env:latest -f server/Dockerfile .
# ✅ Should complete without errors

# PART 5: HF SPACES (Create & Deploy)
# Step 5a: Open browser, go to https://huggingface.co/new-space
#         - SDK: Docker
#         - Name: pattern-puzzle-env
#         - Visibility: Public

# Step 5b: In terminal
git init
git add .
git commit -m "Round 1 OpenEnv Submission"
git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/pattern-puzzle-env
git push -u origin main
# ⏳ Wait 5-10 minutes for deployment

# PART 6: VERIFY SPACE
SPACE_URL="https://YOUR_USERNAME-pattern-puzzle-env.hf.space"
curl -X POST "$SPACE_URL/reset" -H "Content-Type: application/json" -d '{}'
# ✅ Should return 200 response

# PART 7: SUBMIT
# Go to Round 1 portal → Submit space URL
# Done! 🎉

