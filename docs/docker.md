# Docker Guide

This guide explains how to build, run, verify, and troubleshoot the Forecast-Audit Docker container.

## Prerequisites

- Docker installed and running
- Repository cloned locally

## Build Image

From repository root:

```bash
docker build -t forecast-audit-openenv .
```

Alternative helper script:

```bash
bash scripts/build_image.sh
```

## Run Container

Run on default port mapping (`7860:7860`):

```bash
docker run --rm -p 7860:7860 forecast-audit-openenv
```

Run in detached mode:

```bash
docker run -d --name forecast-audit -p 7860:7860 forecast-audit-openenv
```

Stop detached container:

```bash
docker stop forecast-audit
```

## Verify Container Health

```bash
curl http://127.0.0.1:7860/health
```

Expected response:

```json
{"status":"healthy"}
```

Initialize a task:

```bash
curl -X POST http://127.0.0.1:7860/reset \
  -H "Content-Type: application/json" \
  -d '{"difficulty":"easy"}'
```

Submit one action:

```bash
curl -X POST http://127.0.0.1:7860/step \
  -H "Content-Type: application/json" \
  -d '{
    "operation":"impute",
    "target_index":3,
    "predicted_value":135.0,
    "severity":"low",
    "violated_constraints":[],
    "rationale":"Stable +5 ramp"
  }'
```

Read state:

```bash
curl http://127.0.0.1:7860/state
```

## Useful Docker Commands

Show running containers:

```bash
docker ps
```

View container logs:

```bash
docker logs forecast-audit
```

Open shell inside container:

```bash
docker exec -it forecast-audit /bin/bash
```

Remove container:

```bash
docker rm -f forecast-audit
```

Remove image:

```bash
docker rmi forecast-audit-openenv
```

## Troubleshooting

Port already in use:

```bash
lsof -i :7860
```

Container exits immediately:

```bash
docker logs forecast-audit
```

Rebuild without cache:

```bash
docker build --no-cache -t forecast-audit-openenv .
```

## Related Docs

- [Access URLs and Ports](./access-urls-and-ports.md)
- [Local Setup](./local.md)
- [API Reference](./api-reference.md)
- [Troubleshooting](./troubleshooting.md)
