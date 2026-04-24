# FastAPI Service

The service layer moves the LangGraph app from developer-only execution to a callable interface for other systems.

## What The FastAPI Layer Should Own

- request validation
- response schema
- health endpoint
- timeout protection
- error handling
- request-level logging

## Endpoints In This Repository

- `GET /health`
- `POST /invoke`

## Run Locally

```bash
uvicorn deployment.app.api:app --reload --port 8000
```

## Test The API

```bash
curl -X POST http://localhost:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{"query":"Create a LangGraph class plan with labs"}'
```

## Why This Matters

The API layer is where you stop exposing script behavior directly and start offering a controlled service contract.