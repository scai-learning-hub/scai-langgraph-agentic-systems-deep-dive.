# 03. State, Nodes, Edges, and Routing

This is the engineering core of LangGraph. If you design these four things well, the graph usually becomes understandable, testable, and reliable. If you design them poorly, no prompt upgrade will save the system.

## State Design Comes First

Many teams start by thinking about prompts. In production, state should come first.

Why: the state schema decides what information survives across steps, what can be inspected, what routes are possible, and how expensive each hop becomes.

## A Good State Schema Looks Like A Contract

Typical production-friendly state fields include:

- `user_query`
- `task_type`
- `messages`
- `tool_results`
- `review_status`
- `iteration_count`
- `final_answer`
- `errors`
- `trace_id`
- `requires_human_approval`

These fields matter because they answer operational questions:

- What is the task?
- What happened so far?
- Did a tool fail?
- How many loops have run?
- Is the output safe to release?

## State Design Rules

### 1. Keep Fields Purposeful

If a field does not affect execution, debugging, or evaluation, it may not belong in graph state.

### 2. Separate Working State From Long-Term Memory

Short-lived workflow state should not be confused with user memory or historical knowledge. Mixing them causes contamination and token bloat.

### 3. Prefer Structured Fields Over Freeform Dumps

A field like `review_status="approved"` is easier to route on than a paragraph hidden inside `notes`.

### 4. Track Loop Counters And Failure Signals Explicitly

Do not rely on the model to know when to stop. Add fields like `iteration_count`, `max_iterations`, and `last_error`.

### 5. Design For Inspection

If an on-call engineer cannot look at state and understand what happened, the schema is under-designed.

## Node Design: One Job Per Node

Nodes should do one thing well.

Good node responsibilities:

- classify the request
- route the task
- call a specific tool
- draft an answer
- review an answer
- request approval
- finalize output

Bad node responsibilities:

- classify, plan, call tools, summarize, and review all inside one step

Why this matters in real systems: single-responsibility nodes make failures local. Mixed-responsibility nodes create opaque bugs.

## Node Design Checklist

- What inputs does this node require?
- What outputs can it write?
- Can it fail deterministically?
- Should it retry?
- Should it be observable as a distinct step?
- Does it deserve a timeout?
- Should a human be able to inspect it?

If the answer to several of these is yes, the node is likely a real system boundary and should remain explicit.

## Edge Design: Define Allowed Transitions

Edges are more than arrows in a diagram. They are the allowed state transitions of the system.

Examples:

- after classification, go to router
- after research, go back to supervisor
- after review, either finalize or revise
- after three failures, escalate or stop

Edges matter because they make workflow intent visible. They reduce the chance that control flow hides inside prompt text where nobody can test it.

## Conditional Routing: Where System Policy Lives

Conditional routes are some of the most important lines in a LangGraph system. They often encode:

- business policy
- risk policy
- cost policy
- escalation policy
- completion policy

For example, a route function might decide:

- use retrieval for knowledge questions
- use code tooling for implementation tasks
- require approval for external actions
- stop if maximum iterations are reached

That is not just workflow. That is operational policy.

## Deterministic Routing Vs LLM Routing

### Prefer Deterministic Routing When

- the categories are known
- the cost of a wrong route is high
- the signal is easy to compute in code
- you need stable testability

### Use LLM-Assisted Routing When

- the task categories are fuzzy
- language nuance strongly affects the decision
- deterministic heuristics are too brittle
- a fallback or confidence threshold exists

### Best Practice

Use hybrid routing when practical. Let deterministic rules handle obvious cases, and use the model only where judgment is genuinely needed.

Why this matters in real systems: many teams use LLM routing for problems that simple code should handle faster and more reliably.

## Reducers: The Quiet Source Of Many Bugs

Reducers define how updates merge back into state.

They matter most when multiple nodes append to:

- message history
- tool result lists
- audit logs
- reviewer comments
- retrieval results

Without a reducer, a later update may overwrite previous context. With a careless reducer, state can grow forever.

## Reducer Design Rules

- append only what is still useful
- summarize stale details when loops grow long
- separate audit history from prompt history when possible
- do not keep every raw tool output inside model-facing context

Why this matters in real systems: reducer design is where data retention, prompt quality, and cost control meet.

## START And END Are Architectural Signals

`START` is not just where execution begins. It defines the contract for the initial state. `END` is not just where execution stops. It defines what counts as completion.

Good completion criteria:

- a final answer exists
- review status is approved
- loop count is within bounds
- required approvals are complete
- all mandatory tool steps succeeded or were safely bypassed

Bad completion criteria:

- the model said "done"

## Retry Logic In Graphs

Retries should be explicit.

Common patterns:

- retry tool call once on transient network failure
- route to fallback model on provider outage
- request more context on validation failure
- stop after bounded review attempts

Retries should not be infinite, silent, or identical across failure types.

Why this matters in real systems: retry logic that ignores failure cause often makes incidents worse.

## Error Handling Strategy

A mature graph distinguishes at least three error classes:

### 1. Recoverable Technical Errors

Examples: timeout, rate limit, intermittent API failure.

Typical response: retry, backoff, or fallback.

### 2. Recoverable Task Errors

Examples: missing information, weak evidence, failed review.

Typical response: revise, retrieve more data, or ask a clarifying question.

### 3. Non-Recoverable Or Risky Errors

Examples: unsafe instruction, policy violation, ambiguous external action.

Typical response: stop, escalate, or require human approval.

## Observability Needs To Be Designed Into State And Nodes

A practical graph should expose:

- route decisions
- node execution order
- tool invocation metadata
- retry count
- review outcomes
- loop counts
- total latency
- model and tool cost
- error categories

Without these signals, debugging becomes guesswork.

## Evaluation Should Cover Paths, Not Only Outputs

You should evaluate questions like these:

- Did the router choose the right path?
- Did the reviewer improve the answer?
- Did the graph stop too early?
- Did it loop unnecessarily?
- Did the system use a tool when it was not needed?
- Did the supervisor over-delegate?

This is a key shift in thinking. In graph systems, a good final answer can still hide a poor execution path that is too expensive or risky.

## Example State Schema For A Production Agent Workflow

```python
from typing import Annotated, TypedDict


def merge_logs(left: list[str], right: list[str]) -> list[str]:
    return left + right


class AgentState(TypedDict, total=False):
    user_query: str
    task_type: str
    messages: list[str]
    tool_results: dict[str, str]
    review_status: str
    iteration_count: int
    final_answer: str
    last_error: str
    trace_id: str
    audit_log: Annotated[list[str], merge_logs]
```

This schema is not special because it is large. It is useful because each field exists for a reason the system can explain.

## Senior Engineering Guidance

- Keep route functions simple enough to unit test.
- Keep node responsibilities narrow enough to trace.
- Keep state small enough to inspect.
- Keep loops bounded enough to trust.
- Keep tool boundaries explicit enough to audit.

## Architect Guidance

- Design the graph around operating conditions, not only happy-path demos.
- Separate workflow memory, business data, and model context.
- Add human checkpoints at irreversible transitions.
- Treat supervisor design as a throughput and governance concern.
- Define what success, failure, timeout, and escalation mean before deployment.

## Research Direction

The deeper challenge is not whether state, nodes, and edges exist. The challenge is how to optimize them for long-horizon tasks, adaptive routing, memory compression, and robust coordination without losing inspectability.

That is the frontier where practical engineering meets agent systems research.