# 02. LangGraph Core Concepts

This document covers the concepts that matter most when moving from a demo to a durable AI workflow. For each concept, the goal is not just to define it, but to answer a harder question: why does this matter in real systems?

## Graph

### Developer Level

A graph is the workflow. It describes which step runs first, which step runs next, and where the process can branch or stop.

### Senior Engineer Level

The graph is the explicit control plane of the application. It is where you encode sequencing, branching, loops, and stop conditions rather than leaving them implicit inside prompts.

### Architect Level

The graph becomes a system boundary. It separates deterministic execution structure from probabilistic model behavior, making operational control and governance possible.

### Research Level

The open question is how expressive the graph should be before it becomes hard to optimize, verify, or adapt dynamically. More flexibility can improve capability, but it also increases coordination complexity.

Why this matters in real systems: most AI failures happen in orchestration, not just generation. A graph gives you a place to reason about orchestration.

## State

### Developer Level

State is the shared data carried through the workflow. Nodes read from it and write updates into it.

### Senior Engineer Level

State is a contract. If it is poorly designed, nodes become tightly coupled, brittle, and hard to test. Good state design keeps fields explicit and bounded.

### Architect Level

State schema design determines cost, reliability, debuggability, and security. Large or ambiguous state increases token usage, makes failures harder to isolate, and can leak irrelevant context between nodes.

### Research Level

Open problems include compressed memory, retrieval-aware state shaping, and adaptive state summarization for long-horizon tasks.

Why this matters in real systems: bad state design quietly creates expensive, unstable systems.

## Node

### Developer Level

A node is a function that performs one unit of work and returns a state update.

### Senior Engineer Level

Each node should have a clear responsibility, a predictable input contract, and a narrow output shape. Nodes that do classification, tool use, planning, and response generation all at once are hard to debug.

### Architect Level

Nodes define operational boundaries. They are the places where you can add retries, metrics, tracing, approvals, and fault isolation.

### Research Level

An open question is how much reasoning should be localized to a node versus distributed across multi-step planning structures.

Why this matters in real systems: node design determines whether a workflow is inspectable or opaque.

## Edge

### Developer Level

An edge connects one node to the next.

### Senior Engineer Level

Edges make control flow visible. They help you answer a simple but operationally critical question: what can happen next?

### Architect Level

Edges are part of the allowed state transition model. They can be reviewed, tested, and constrained. This matters for safety and auditability.

### Research Level

More expressive transition logic can improve adaptability, but it also creates verification challenges in larger agent systems.

Why this matters in real systems: without explicit edges, teams often cannot explain how a bad execution path occurred.

## Conditional Edge

### Developer Level

A conditional edge chooses the next node based on state.

### Senior Engineer Level

This is where routing logic lives. It should usually be simple, bounded, and testable. Avoid hiding routing logic inside long prompts if deterministic code can do it better.

### Architect Level

Conditional routing is one of the main places where system policy is encoded: safe path, escalation path, retry path, or end state.

### Research Level

Open directions include learned routing, cost-aware routing, and hybrid policies that combine model judgment with deterministic constraints.

Why this matters in real systems: routing quality strongly affects latency, cost, and failure rate.

## Reducer

### Developer Level

A reducer defines how updates are merged into the existing state.

### Senior Engineer Level

Reducers matter when multiple nodes add to lists, logs, or message histories. Without an intentional merge policy, state updates can overwrite each other or grow uncontrollably.

### Architect Level

Reducers are a hidden reliability surface. They influence state growth, replay behavior, and the ability to reconstruct execution history.

### Research Level

There is room for smarter reducers that summarize, compress, or selectively retain state based on downstream need.

Why this matters in real systems: poor merging rules often create silent data loss or token bloat.

## START And END

### Developer Level

`START` marks the entry point. `END` marks termination.

### Senior Engineer Level

They force you to be explicit about how execution begins and what success or completion means.

### Architect Level

Clear start and end semantics help define SLAs, timeouts, retries, and resumability. They are part of the operational contract.

### Research Level

In long-running agents, termination itself becomes a research problem. The system must decide whether the task is truly complete or only appears complete.

Why this matters in real systems: ambiguous termination is a common cause of infinite loops and wasted spend.

## Supervisor Pattern

### Developer Level

A supervisor is a node or agent that decides which specialized worker should act next.

### Senior Engineer Level

The supervisor pattern helps organize complex workflows, but it can become a bottleneck if every decision requires one central controller.

### Architect Level

A supervisor is useful when teams need policy control, bounded delegation, and clear responsibility separation. It is risky when used as a catch-all decision maker with vague worker roles.

### Research Level

The hard problem is not only routing but maintaining efficient coordination without creating repetitive, expensive communication between agents.

Why this matters in real systems: supervisors help manage complexity, but poor supervisor design centralizes failure.

## Router Pattern

### Developer Level

A router chooses one path among several based on the current request or state.

### Senior Engineer Level

Routers are often better than supervisors for simpler problems because the policy can be deterministic and cheap.

### Architect Level

Choosing router versus supervisor is a system design trade-off: deterministic routing improves control and predictability, while supervisory control improves flexibility at higher cost.

### Research Level

Advanced routing asks whether the route should depend on uncertainty, expected cost, model confidence, or external signals.

Why this matters in real systems: many multi-agent designs should actually be routers.

## Tool-Using Agents

### Developer Level

These are nodes or agents that can call external functions like calculators, retrievers, or APIs.

### Senior Engineer Level

Tools should be deterministic where possible, strongly typed when practical, and bounded by clear failure handling.

### Architect Level

Tools are trust boundaries. Every tool introduces correctness, latency, security, and observability concerns. A graph should make those boundaries explicit.

### Research Level

Reliable tool grounding remains a hard problem. Models can misuse tools, misread tool outputs, or call the wrong tool at the wrong time.

Why this matters in real systems: tools are where agent systems touch the real world, so mistakes become operational issues.

## Review Loop

### Developer Level

A review loop lets the system draft, check, and revise before returning an answer.

### Senior Engineer Level

The loop needs bounded iterations and explicit approval criteria. Otherwise it will spin, drift, or over-edit.

### Architect Level

Review loops improve quality only when review criteria are aligned with production goals such as policy, factuality, or format compliance.

### Research Level

Self-critique remains unreliable. Good critique can improve output, but poorly designed critique often amplifies error or creates endless refinement.

Why this matters in real systems: review loops can improve reliability, but unbounded review loops are costly failure generators.

## Human-In-The-Loop

### Developer Level

This means a person can inspect, approve, reject, or edit workflow state before execution continues.

### Senior Engineer Level

Human checkpoints are most useful at irreversible or high-risk transitions such as sending external messages, modifying code, or escalating cases.

### Architect Level

Human-in-the-loop is a governance design, not just a UI feature. It defines where autonomy stops and accountability begins.

### Research Level

An open question is how to design collaboration patterns where humans guide agent behavior without becoming throughput bottlenecks.

Why this matters in real systems: risky automation without approval gates eventually causes preventable incidents.

## Checkpointing

### Developer Level

Checkpointing saves workflow state so execution can resume later.

### Senior Engineer Level

This is useful for long-running jobs, human approval pauses, retriable failures, and inspection of partial progress.

### Architect Level

Checkpointing is part of durability strategy. It changes how you think about fault tolerance, recovery, and user experience in interrupted workflows.

### Research Level

Long-horizon agents need better checkpoint semantics for partial plans, external tool dependencies, and memory consistency.

Why this matters in real systems: without checkpoints, long workflows often fail in ways that force full restarts.

## Memory

### Developer Level

Memory is the information the system keeps across steps or across sessions.

### Senior Engineer Level

Short-term working memory and long-term recalled memory should usually be separated. Putting everything in one growing state object causes drift and waste.

### Architect Level

Memory architecture affects privacy, relevance, token cost, and user trust. The central question is not only what to remember, but what to forget.

### Research Level

Open problems include durable semantic memory, memory editing, memory compression, and retrieval strategies for long-horizon task performance.

Why this matters in real systems: memory that grows without design becomes both a quality problem and a compliance problem.

## Retry Logic And Error Handling

### Developer Level

Retries handle temporary failures. Error handling decides what the system should do when a node or tool fails.

### Senior Engineer Level

Retries should be selective and bounded. Not every failure deserves another attempt, especially if the failure is deterministic.

### Architect Level

Retry policies interact with cost, latency, and safety. Systems need clear fallback behavior, timeout rules, and escalation paths.

### Research Level

Adaptive retry strategies that reason about failure cause, expected value, and confidence remain an active area of design.

Why this matters in real systems: uncontrolled retries create noisy failures, duplicate actions, and cost spikes.

## Observability

### Developer Level

Observability means you can see what the workflow did and why.

### Senior Engineer Level

At minimum, log node entry, node exit, route decisions, tool calls, latency, errors, and final outcomes.

### Architect Level

Observability is essential for reliability engineering, auditing, performance optimization, and model governance.

### Research Level

Future observability needs will likely include richer causal tracing, policy attribution, and better ways to compare reasoning paths across runs.

Why this matters in real systems: if you cannot inspect the path, you cannot improve the system responsibly.

## Evaluation

### Developer Level

Evaluation checks whether the workflow is producing useful results.

### Senior Engineer Level

The important shift is evaluating paths, not just final answers. You need to know whether the router chose well, whether the reviewer helped, and whether tool use improved the result.

### Architect Level

Evaluation strategy should connect product quality, operational risk, and cost. It is part of system design, not a separate afterthought.

### Research Level

Evaluation of agent systems remains difficult because outcomes depend on interaction sequences, memory, external tools, and hidden failure modes.

Why this matters in real systems: without evaluation, teams optimize demos and guess about production quality.

## Multi-Agent Coordination

### Developer Level

Multi-agent coordination means multiple specialized workers collaborate through shared state and explicit transitions.

### Senior Engineer Level

The key implementation concern is responsibility clarity. If two agents do roughly the same thing, the system wastes tokens and increases confusion.

### Architect Level

The central trade-off is specialization versus overhead. More agents can improve modularity, but they also add communication cost, latency, and failure surfaces.

### Research Level

Open challenges include stable coordination protocols, role formation, shared memory management, and long-horizon plan execution.

Why this matters in real systems: multi-agent systems are powerful when specialization is real, and wasteful when it is not.

## Final Teaching Summary

LangGraph should be taught not as syntax, but as a way to design reliable AI workflows. The syntax is useful, but the deeper lesson is architectural: define state clearly, keep nodes responsible, route intentionally, bound loops, save progress, observe execution, and evaluate the whole workflow rather than trusting a single model call.