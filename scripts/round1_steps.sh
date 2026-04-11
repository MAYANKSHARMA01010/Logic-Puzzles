#!/bin/bash
# Copy-paste commands for Round 1

cd ~/Desktop/Projects/Forecast-Audit
source .venv/bin/activate
cp .env.example .env
pip install -r requirements.txt
python validate.py
