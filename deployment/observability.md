# Observability

Observability for an agent system must cover both the API layer and the graph layer.

## API-Level Signals

- request start and finish
- request latency
- timeout events
- validation failures
- internal server failures

## Graph-Level Signals

- node execution sequence
- route decisions
- iteration count
- tool usage
- model selection
- final status

## Tracing And Logging

Use logs for durable operational records. Use traces for execution-path inspection. Mature production systems need both.

## Why This Matters

Without observability, you may know the answer was bad but still not know whether the router, tool call, timeout, or reviewer caused the problem.