# Round 1 Checklist

- Run `./scripts/validate-submission.sh`
- Run `python validate.py`
- Run `docker build -t pattern-puzzle-env:latest .`
- Run `openenv validate`
- Run `inference.py` once with a valid token
- Deploy to Hugging Face Spaces
- Test `POST /reset` on the live Space
- Test `POST /step` on the live Space
