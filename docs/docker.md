# Docker

## Build the image

```bash
docker build -t pattern-puzzle-env:latest -f server/Dockerfile .
```

## Run the container

```bash
docker run --rm -p 7860:7860 pattern-puzzle-env:latest
```

## Notes

- The server must listen on port 7860
- Hugging Face Spaces will use the Dockerfile in `server/`
