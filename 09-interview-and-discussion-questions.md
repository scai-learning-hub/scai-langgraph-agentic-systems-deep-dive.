# 09. Interview and Discussion Questions

## LangGraph Interview Questions

These questions are designed for real technical discussions, not trivia. A strong answer should connect syntax to system behavior, and system behavior to production trade-offs.

## Beginner

### 1. What problem does LangGraph solve that a plain LangChain chain does not?

What strong answer should mention: explicit workflow control, shared state, conditional routing, loops, checkpoints, and the difference between connecting components and orchestrating durable execution.

Weak answer red flags: describing LangGraph as only "LangChain but better" or talking only about graphs in an abstract sense.

Follow-up question: when would a plain chain still be the better choice?

### 2. What are state, nodes, and edges in LangGraph?

What strong answer should mention: state as shared workflow data, nodes as units of work that read and update state, and edges as explicit transitions between steps.

Weak answer red flags: defining the pieces without explaining why they matter to control flow and debugging.

Follow-up question: why is state design often more important than prompt wording in a graph system?

### 3. What is a conditional edge and when would you use one?

What strong answer should mention: route decisions based on state, branching to different nodes, and typical uses such as task classification, retry handling, or review outcomes.

Weak answer red flags: saying it is only for convenience or failing to connect it to system policy.

Follow-up question: when would deterministic routing be better than model-based routing?

### 4. What do START and END represent?

What strong answer should mention: the entry point and termination point of the graph, plus the need for explicit start-state and completion semantics.

Weak answer red flags: treating them as syntax only and ignoring loop control or completion criteria.

Follow-up question: what can go wrong if END is effectively defined as "the model said it was done"?

### 5. Why are reducers useful in LangGraph?

What strong answer should mention: controlled merging of state updates, especially for logs, message history, and accumulated outputs.

Weak answer red flags: not understanding overwrite vs append behavior or ignoring token growth concerns.

Follow-up question: how can a bad reducer design create production problems?

### 6. When is LangGraph unnecessary?

What strong answer should mention: short, linear, stateless workflows with no meaningful branching, retries, checkpoints, or review loops.

Weak answer red flags: saying LangGraph should be used for every LLM application.

Follow-up question: what signals tell you a simple chain is about to become a graph problem?

## Intermediate

### 7. How would you design state for a tool-using agent workflow?

What strong answer should mention: fields for query, tool decision, tool input, tool output, loop count, error state, and final answer, with structured fields for routing.

Weak answer red flags: storing everything in a raw message list without explicit operational fields.

Follow-up question: which state fields belong in prompts and which should stay out of prompt context?

### 8. Router pattern vs supervisor pattern: how do you choose?

What strong answer should mention: routers for stable and testable branching, supervisors for iterative delegation when next steps depend on accumulated state.

Weak answer red flags: choosing supervisor by default because it sounds more advanced.

Follow-up question: what is the operational cost of a supervisor-heavy design?

### 9. How do you prevent infinite loops in a graph workflow?

What strong answer should mention: max iterations, explicit completion rules, loop counters in state, review criteria, and escalation or final best-effort exits.

Weak answer red flags: trusting the model to stop on its own.

Follow-up question: what telemetry would help you detect a loop issue in production?

### 10. How would you implement a review loop in LangGraph?

What strong answer should mention: draft node, review node, structured decision, revise path, bounded loop count, and quality criteria tied to production goals.

Weak answer red flags: saying "just ask the model to review itself" without bounds or acceptance criteria.

Follow-up question: when can a review loop make the output worse instead of better?

### 11. Why should tools be deterministic where possible?

What strong answer should mention: easier debugging, more stable execution, lower ambiguity, and cleaner separation between reasoning and external action.

Weak answer red flags: treating tools as just more prompts.

Follow-up question: what extra controls do you need when a tool itself is nondeterministic?

### 12. What does checkpointing buy you in a production graph?

What strong answer should mention: resume after failure, pause for approval, durable long-running workflows, and better incident recovery.

Weak answer red flags: describing checkpointing as only a developer convenience.

Follow-up question: why is in-memory checkpointing not enough for production?

## Advanced

### 13. How do you separate prompt logic from orchestration logic?

What strong answer should mention: keep prompts focused on local reasoning tasks and keep routing, retries, approvals, and budgets in the graph or deterministic code.

Weak answer red flags: giant prompts that silently encode workflow policy.

Follow-up question: what symptoms suggest orchestration logic has leaked into prompts?

### 14. How do you evaluate a LangGraph system beyond final answer quality?

What strong answer should mention: path evaluation, route quality, tool usefulness, review impact, latency, cost, and failure classification.

Weak answer red flags: judging the system only by whether the final answer sounds good.

Follow-up question: why can a "good" answer still hide a bad graph execution?

### 15. How would you design retries and timeouts for graph nodes?

What strong answer should mention: failure-type-specific retries, node-level timeouts, fallback behavior, and explicit error state updates.

Weak answer red flags: retrying every error the same way or ignoring timeout budgets.

Follow-up question: which failures should never be retried automatically?

### 16. How do you avoid context contamination between agents?

What strong answer should mention: role-scoped context, minimal state exposure per node, and separation between audit logs and prompt-facing context.

Weak answer red flags: giving every agent the full raw transcript all the time.

Follow-up question: why does a reviewer lose value if it sees the exact same bloated context as the writer?

### 17. What makes a good agent boundary?

What strong answer should mention: clear responsibility, unique value, testable inputs and outputs, and minimal overlap with other agents.

Weak answer red flags: roles defined by vague labels like "thinker" and "helper".

Follow-up question: what evidence would convince you to merge two agents into one?

### 18. How would you design observability for a LangGraph deployment?

What strong answer should mention: node traces, route decisions, tool payload metadata, latency, cost, retries, approvals, and persistent logs.

Weak answer red flags: relying on final output logs only.

Follow-up question: what is the difference between tracing and operational logging in this context?

## Architect-Level

### 19. How do you decide between a single-agent and multi-agent architecture?

What strong answer should mention: specialization value, coordination overhead, governance complexity, cost, latency, and the need for a strong baseline comparison.

Weak answer red flags: choosing multi-agent because the task feels important or open-ended.

Follow-up question: what metrics would you compare between the single-agent and multi-agent versions?

### 20. How would you place LangGraph inside a production system architecture?

What strong answer should mention: LangGraph as orchestration between API/frontend, model providers, tools, retrieval, checkpoint store, observability, and evaluation systems.

Weak answer red flags: treating the graph as if it were the whole platform.

Follow-up question: what components outside LangGraph are essential for a reliable deployment?

### 21. How do you design human approval gates for risky actions?

What strong answer should mention: action-based risk classes, pause and resume semantics, approver metadata, audit trail, and clear escalation paths.

Weak answer red flags: adding human review only as a UI afterthought.

Follow-up question: which graph transitions would you classify as irreversible?

### 22. How would you structure memory in a long-running agent system?

What strong answer should mention: separation of working state, session continuity, and long-term memory or retrieval, plus retention and forgetting strategy.

Weak answer red flags: storing everything forever in one shared context buffer.

Follow-up question: how do memory design mistakes show up in latency and answer quality?

### 23. How do you prevent the supervisor from becoming a bottleneck?

What strong answer should mention: deterministic routing for obvious decisions, narrower supervisor responsibilities, cost-aware delegation, and throughput-aware design.

Weak answer red flags: letting the supervisor mediate every small step.

Follow-up question: what is the difference between useful supervision and over-centralization?

### 24. What governance concerns appear in production agent workflows?

What strong answer should mention: auditability, approval, accountability, tool permissions, logging, trace retention, and safe action boundaries.

Weak answer red flags: reducing governance to prompt safety alone.

Follow-up question: how would you prove after the fact why a risky action happened?

## Research-Level

### 25. Why is multi-agent coordination still an open problem?

What strong answer should mention: communication overhead, redundant work, role drift, shared memory conflicts, and lack of stable credit assignment.

Weak answer red flags: assuming more agents naturally means more intelligence.

Follow-up question: what would a meaningful coordination benchmark need to measure?

### 26. What are the benefits and limits of separating planning from execution?

What strong answer should mention: improved structure and delegation, but also stale plans, environment changes, and expensive re-planning.

Weak answer red flags: assuming a planner always improves execution quality.

Follow-up question: how should a system decide when to abandon a plan and re-plan?

### 27. What are the limits of self-reflection and critique loops?

What strong answer should mention: critique can help but may also reinforce bad assumptions, overfit to format, or create endless low-value revisions.

Weak answer red flags: assuming self-critique is inherently reliable.

Follow-up question: how would you test whether a critique loop is helping in practice?

### 28. Why are memory compression and context engineering hard research problems?

What strong answer should mention: preserving task-relevant information while reducing token cost, avoiding contamination, and deciding what to forget.

Weak answer red flags: suggesting that bigger context windows remove the problem entirely.

Follow-up question: what information would you compress aggressively, and what would you preserve exactly?

### 29. What does cost-aware routing add beyond ordinary task routing?

What strong answer should mention: selecting paths based on expected value, latency, risk, and budget, not only task category.

Weak answer red flags: treating cost as a finance issue disconnected from architecture.

Follow-up question: when is it rational to spend more on a stronger path?

### 30. Why do agent systems need simulation and benchmarking beyond static prompt tests?

What strong answer should mention: interactive environments, long-horizon execution, tool failures, path dependence, repeatability, and recovery behavior.

Weak answer red flags: assuming one-shot benchmark scores tell you how an agent system behaves under real workflow conditions.

Follow-up question: what would you include in a benchmark for a tool-using, checkpointed, multi-step agent?

## How To Use These Questions

Use these prompts to assess whether someone understands LangGraph as a workflow system rather than as a syntax surface. Strong candidates usually connect state, routing, reliability, evaluation, and governance into one coherent mental model.