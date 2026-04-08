# Logic-Puzzles

An AI pattern puzzle environment built with OpenEnv. The agent sees a sequence, guesses the next value, and earns reward based on difficulty and speed.

## Start Here

- [Project overview](docs/overview.md)
- [Install dependencies](docs/installation.md)
- [Run locally](docs/local.md)
- [Run with Docker](docs/docker.md)
- [Submission guide](docs/submission.md)
- [Round 1 checklist](docs/round1/checklist.md)
- [Round 1 quick submit](docs/round1/quick-submit.md)

## Main Files

- `inference.py` runs the baseline agent
- `server/app.py` exposes the environment API
- `server/environment.py` holds the tasks and rewards
- `openenv.yaml` describes the environment for validation
- `scripts/validate-submission.sh` checks the submission locally

## Quick Commands

```bash
python validate.py
source scripts/setup_env.sh
.venv/bin/python -m uvicorn server.app:app --host 0.0.0.0 --port 7860 --reload
.venv/bin/python inference.py
```