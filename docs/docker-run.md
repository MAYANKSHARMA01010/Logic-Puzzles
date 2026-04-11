# Docker Run

Build and run the project in Docker.

```bash
docker build -t forecast-audit-openenv .
docker run --rm -p 7860:7860 forecast-audit-openenv
```

Check service health:

```bash
curl http://localhost:7860/health
```