# Submission

## Validation

```bash
chmod +x scripts/validate-submission.sh
./scripts/validate-submission.sh
```

## Deploy to Hugging Face Spaces

1. Create a new Space
2. Choose Docker
3. Push the repo
4. Wait for the build to finish
5. Check `/reset` on the Space URL

## Required files

- `openenv.yaml`
- `inference.py`
- `requirements.txt`
- `server/Dockerfile`
- `README.md`
- `.env.example`
