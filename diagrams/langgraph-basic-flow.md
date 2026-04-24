# LangGraph Basic Flow

This is the smallest useful mental model for LangGraph. A user request enters the workflow, an agent decides whether it has enough information, and a tool loop runs only when needed.

```mermaid
flowchart TD
    A[User Input] --> B[Agent Node]
    B --> C{Need Tool?}
    C -->|Yes| D[Tool Node]
    D --> B
    C -->|No| E[Final Answer]
```

## Why This Matters

- It shows that a graph is about controlled execution, not just calling a model.
- It keeps tool usage explicit.
- It demonstrates a bounded loop pattern that can later gain retries, review, and checkpointing.