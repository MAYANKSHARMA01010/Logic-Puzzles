---
title: Forecast Audit OpenEnv
emoji: 📈
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# Forecast Audit OpenEnv

Forecast Audit OpenEnv is a mathematically-oriented, real-world environment for training and evaluating agents on numerical quality-assurance tasks.

Instead of solving toy puzzles, the agent acts like an analyst who must inspect metric series, repair missing values, identify anomalous points, and decide whether a forecast should be accepted, repaired, or escalated.

## Why this is useful

Humans do this kind of work every day in:
- quantitative research and trading
- energy and grid operations
- business forecasting and operations planning
- analytics QA and data quality review

This environment measures whether an agent can:
- infer numerical structure from data
- respect explicit constraints
- choose the right workflow action
- handle uncertainty responsibly

## Tasks

### Easy — missing-value imputation
A stable operational series has one missing point. The agent should impute the value.

### Medium — anomaly repair
A financial time series contains one obviously corrupted point. The agent should flag or repair it.

### Hard — constraint-based forecast validation
An energy demand forecast violates a physical/operational rule. The agent should identify the constraint and escalate.

## Action space

The action is a typed JSON object:

```json
{
  "operation": "impute",
  "target_index": 3,
  "predicted_value": 135.0,
  "severity": "low",
  "violated_constraints": [],
  "rationale": "The sequence rises by 5 each hour, so the missing point is 135."
}
```

## Observation space

Each observation includes:
- task id and difficulty
- domain and metric name
- timestamps and values
- issue type
- explicit constraints
- analyst note
- history summary
- step counter

## Reward design

Rewards are dense and graded on:
- correct operation choice
- correct target index
- numerical accuracy of the repaired value
- severity classification
- correct violated-constraint citation
- rationale quality
- efficiency

Penalties apply for destructive or obviously wrong actions, such as accepting invalid data.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python validate.py
uvicorn server.app:app --host 0.0.0.0 --port 7860 --reload
```

## Baseline evaluation

Heuristic baseline:

```bash
python inference.py
```

OpenAI API baseline:

```bash
export OPENAI_API_KEY=your_key_here
export MODEL_NAME=gpt-4o-mini
python inference.py
```

## Docker

```bash
docker build -t forecast-audit-openenv .
docker run --rm -p 7860:7860 forecast-audit-openenv
```

## Main files

- `models.py` — typed Pydantic models
- `server/environment.py` — task specs, reward shaping, graders
- `server/app.py` — FastAPI service
- `client.py` — async client helper
- `inference.py` — baseline scoring script
- `validate.py` — local validation checks
- `openenv.yaml` — environment metadata

## Notes

The manifest fields in `openenv.yaml` are written to be readable and close to typical OpenEnv packaging. If your installed validator expects slightly different field names, adjust the manifest field names to match your local `openenv validate` version without changing the environment logic.