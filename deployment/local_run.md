# Local Run

Local script execution is the first stage of productionization. The goal is not scale. The goal is to verify graph behavior before a service boundary is introduced.

## What To Validate Locally

- graph compiles cleanly
- node transitions match expectations
- max iteration protection works
- outputs are stable enough to wrap behind an API

## Commands

```bash
pip install -r requirements.txt
python examples/04_multi_agent_supervisor.py
```

## Why This Matters

If a workflow is hard to reason about in a local script, putting it behind FastAPI will only make debugging slower.