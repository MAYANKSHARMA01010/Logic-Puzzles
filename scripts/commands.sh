#!/bin/bash
# Quick commands for local setup and submission

cd ~/Desktop/Projects/Logic-Puzzles
source .venv/bin/activate
cp .env.example .env
chmod +x scripts/validate-submission.sh
./scripts/validate-submission.sh
