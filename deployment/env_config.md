# Environment Configuration

Configuration should come from environment variables so the same code can run in development, staging, and production without source changes.

## Variables Used In This Repository

- `GROQ_API_KEY`
- `MODEL_NAME`
- `MAX_ITERATIONS`
- `REQUEST_TIMEOUT_SECONDS`
- `ENVIRONMENT`

## Example `.env`

```bash
GROQ_API_KEY=your_key_here
MODEL_NAME=llama-3.1-8b-instant
MAX_ITERATIONS=4
REQUEST_TIMEOUT_SECONDS=45
ENVIRONMENT=development
```

## Why This Matters

Hardcoded configuration makes deployments brittle and secrets unsafe. Environment-driven configuration is a basic production requirement.