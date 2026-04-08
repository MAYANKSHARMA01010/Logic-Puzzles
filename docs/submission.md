# Submission

## Validation

```bash
chmod +x scripts/validate-submission.sh
./scripts/validate-submission.sh
```

## Deploy to Hugging Face Spaces

1. Create a new Space
2. Choose Docker
3. Push this repo to the Space remote
4. Add required Space Secrets in Settings -> Variables and secrets:
	 - `HF_TOKEN`
	 - `API_BASE_URL` (for example `https://router.huggingface.co/v1`)
	 - `MODEL_NAME` (for example `Qwen/Qwen2.5-72B-Instruct`)
	 - `IMAGE_NAME` (if your inference flow uses it)
5. Wait for the build to finish
6. Open `/docs` on the Space URL and test endpoints

## API smoke tests (after deploy)

Replace `[<SPACE_URL>](https://huggingface.co/spaces/Manku69/logic-puzzles)` with your live URL, for example `https://manku69-logic-puzzles.hf.space`.

```bash
curl <SPACE_URL>/health

curl -X POST [<SPACE_URL>](https://huggingface.co/spaces/Manku69/logic-puzzles)/reset \
	-H "Content-Type: application/json" \
	-d '{"difficulty":"easy"}'

curl -X POST [<SPACE_URL>](https://huggingface.co/spaces/Manku69/logic-puzzles)/step \
	-H "Content-Type: application/json" \
	-d '{"guess":"8"}'
```

## Required files

- `openenv.yaml`
- `inference.py`
- `requirements.txt`
- `Dockerfile`
- `README.md`
- `.env.example`
