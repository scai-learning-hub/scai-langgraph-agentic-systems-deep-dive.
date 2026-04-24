# Docker

Containerization makes the API runtime reproducible across machines and deployment targets.

## Build The Image

```bash
docker build -t langgraph-agent-api .
```

## Run The Container

```bash
docker run --env-file .env -p 8000:8000 langgraph-agent-api
```

## Compose

```bash
docker compose up --build
```

## Why This Matters

If the service only works on the original developer machine, it is not deployment-ready. Docker reduces environment drift and makes CI and production rollout more predictable.