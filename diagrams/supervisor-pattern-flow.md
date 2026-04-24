# Supervisor Pattern Flow

This diagram shows a classic supervisor-driven multi-agent workflow. One controller routes work to specialists and decides when the system is ready to finalize.

```mermaid
flowchart TD
    A[User Query] --> B[Supervisor Agent]
    B --> C{Route Task}
    C -->|Research| D[Research Agent]
    C -->|Code| E[Coding Agent]
    C -->|Review| F[Reviewer Agent]
    D --> B
    E --> B
    F --> B
    B --> G[Final Agent]
    G --> H[END]
```

## Why This Matters

- It makes delegation explicit.
- It shows how specialists can loop back through a controller.
- It highlights where bottlenecks and governance concerns usually appear.