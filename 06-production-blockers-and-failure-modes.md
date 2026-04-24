# 06. Production Blockers and Failure Modes

This section is intentionally blunt. Most agent projects do not fail because nobody knew how to call an LLM. They fail because workflow reliability, cost control, observability, and governance were not designed early enough.

Below are the blockers that appear repeatedly in real systems. For each one, the question is the same: what actually goes wrong in production, how do you notice it, and what should you do about it?

## 1. Infinite Loops

What happens: the graph keeps cycling between agent, tool, reviewer, or supervisor nodes and never settles.

Why it happens: there is no explicit `max_iterations`, no strong completion rule, or the review criteria keep moving.

How to detect it: repeated trace patterns, rising token spend per request, long tail latency, and runs that revisit the same nodes excessively.

How to fix it: add bounded loop counters, stable acceptance criteria, and hard stops that route to escalation or final best-effort output.

Production recommendation: track per-run iteration counts and alert on unusual loop depth.

## 2. Bad State Design

What happens: nodes become brittle, context gets overwritten, and routing decisions depend on vague text instead of structured fields.

Why it happens: teams treat state as a dump of messages rather than a contract for execution.

How to detect it: hard-to-debug failures, duplicated logic across nodes, and route functions that parse long paragraphs to infer simple facts.

How to fix it: redesign state around explicit fields like `task_type`, `review_status`, `iteration_count`, and `final_answer`.

Production recommendation: review the state schema the same way you would review an API contract.

## 3. Unclear Agent Responsibility

What happens: multiple agents do overlapping work, outputs sound repetitive, and nobody can explain why one agent exists.

Why it happens: roles were created for conceptual neatness rather than real specialization.

How to detect it: two agents produce near-identical summaries, reviewer rewrites instead of reviewing, or supervisor keeps bouncing between similar workers.

How to fix it: define one clear responsibility per agent and remove agents that do not create measurable value.

Production recommendation: if you cannot explain each agent's unique decision or capability boundary, collapse the design.

## 4. Too Many Agents For Simple Tasks

What happens: latency rises, token cost spikes, and the system becomes harder to test than the business problem requires.

Why it happens: multi-agent design is adopted before a strong single-agent baseline exists.

How to detect it: a simpler router or single-agent workflow solves the same task with similar quality.

How to fix it: benchmark against a single-agent baseline and only keep specialization that improves quality, safety, or maintainability.

Production recommendation: treat multi-agent orchestration as an optimization that must earn its complexity.

## 5. Tool Failure

What happens: external calls fail, return malformed data, or take too long, causing incomplete or misleading final answers.

Why it happens: network instability, provider outages, schema mismatches, or weak timeout handling.

How to detect it: spikes in node errors, fallback usage, and partial answers that omit tool-derived evidence.

How to fix it: validate tool outputs, classify failures as transient or permanent, and add retries only for recoverable errors.

Production recommendation: every tool should have timeout, error classification, and telemetry from day one.

## 6. Hallucinated Tool Outputs

What happens: the model claims a tool returned something that the tool never produced.

Why it happens: tool outputs are copied into prompts loosely, and the model is allowed to paraphrase them as if they were facts.

How to detect it: compare logged tool payloads with final answers and reviewer notes.

How to fix it: keep tool outputs structured, reference them explicitly, and add validation where possible.

Production recommendation: treat tool outputs as auditable records, not informal model memory.

## 7. Prompt Drift

What happens: behavior changes over time as prompts accrete exceptions, edge cases, and copied instructions.

Why it happens: teams patch prompts instead of redesigning nodes, routes, or state.

How to detect it: increasing inconsistency between similar tasks, fragile regressions, and prompts that try to handle policy, routing, review, and formatting at once.

How to fix it: move workflow logic into the graph, reduce prompt scope, and version prompts alongside tests.

Production recommendation: keep prompts narrow and treat them as one component of the system, not the whole control plane.

## 8. No Evaluation Strategy

What happens: the team ships based on demo quality and cannot prove whether the workflow improved or regressed.

Why it happens: evaluation is postponed until after the architecture is already unstable.

How to detect it: arguments about quality are anecdotal, and no path-level metrics exist.

How to fix it: define offline cases, path-quality checks, cost metrics, and human review benchmarks.

Production recommendation: evaluate routing, tool use, and review effects separately from final answer quality.

## 9. No Observability

What happens: incidents cannot be diagnosed because nobody knows which node ran, what route was chosen, or which tool failed.

Why it happens: teams log final outputs only and ignore intermediate execution.

How to detect it: support tickets require reruns to understand behavior, and on-call engineers cannot explain a bad result from logs alone.

How to fix it: trace node entry and exit, route decisions, tool invocations, retries, latency, and cost.

Production recommendation: if a run cannot be reconstructed from telemetry, the system is under-observed.

## 10. No Cost Control

What happens: a workflow works functionally but becomes too expensive to operate at volume.

Why it happens: no token budgeting, unbounded loops, unnecessary agent handoffs, or oversized state.

How to detect it: high cost variance across similar requests and unexpected spend growth after feature additions.

How to fix it: add model tiers, path budgets, summarized state, and tool-use thresholds.

Production recommendation: cost should be a first-class routing input, not a monthly surprise.

## 11. No Timeout Strategy

What happens: slow providers or tools cause workflows to stall until the user experience degrades or the request times out upstream.

Why it happens: node-level and tool-level timeouts were never defined.

How to detect it: long-running requests with little signal about where the delay occurred.

How to fix it: define timeouts per node type, add fallback behavior, and record timeout reason in state.

Production recommendation: every external dependency should have an explicit timeout budget and fallback policy.

## 12. No Human Approval For Risky Actions

What happens: the system sends messages, changes records, triggers workflows, or writes code without appropriate review.

Why it happens: teams optimize for autonomy before defining risk classes.

How to detect it: near misses, policy breaches, or user complaints about unauthorized actions.

How to fix it: insert human checkpoints before irreversible or high-impact transitions.

Production recommendation: define approval gates by action class, not by vague intuition.

## 13. Weak Memory Design

What happens: the system forgets important facts, remembers irrelevant facts, or leaks stale context into new tasks.

Why it happens: short-term state, user memory, and historical memory are mixed together.

How to detect it: inconsistent answers, cross-session contamination, and rising token counts from accumulated history.

How to fix it: separate working state from long-term memory and design retrieval rules explicitly.

Production recommendation: memory architecture should answer both what to remember and what to forget.

## 14. Large State Causing Token Bloat

What happens: prompts become oversized, latency increases, and model performance degrades because the important signal is diluted.

Why it happens: every intermediate message, tool payload, and reviewer note is stuffed into model-facing context.

How to detect it: prompt size grows with loop count, and answer quality drops even as more context is included.

How to fix it: summarize aggressively, separate audit logs from prompt context, and retain only route-relevant details.

Production recommendation: state should be inspectable and economical, not a transcript landfill.

## 15. No Fallback Model Or Retry Policy

What happens: provider outages or intermittent failures become full workflow failures.

Why it happens: the system assumes the primary model is always available and always sufficient.

How to detect it: outage-driven incident spikes and no graceful degradation path.

How to fix it: define fallback providers or smaller models for degraded operation, and apply retries only where useful.

Production recommendation: provider reliability is part of architecture, not just vendor choice.

## 16. No Testing Of Graph Paths

What happens: a rarely used route breaks silently until a real request finds it.

Why it happens: only the happy path is tested.

How to detect it: branches exist in code but have no fixtures, assertions, or regression cases.

How to fix it: test route functions, loop exit conditions, fallback paths, and error transitions explicitly.

Production recommendation: path coverage matters more than line coverage in orchestration-heavy systems.

## 17. Supervisor Becoming A Bottleneck

What happens: every step funnels through one high-cost decision-maker, creating throughput and latency pressure.

Why it happens: the supervisor owns too many choices, even simple deterministic ones.

How to detect it: most node time is spent in supervision rather than useful specialist work.

How to fix it: move obvious decisions into deterministic routers and reserve supervisor judgment for genuinely ambiguous coordination.

Production recommendation: supervisors should coordinate complexity, not create it.

## 18. Agents Repeating Each Other

What happens: multiple agents restate similar content with minor wording changes.

Why it happens: agent prompts are not differentiated and state does not enforce unique roles.

How to detect it: outputs have high semantic overlap and little new information per hop.

How to fix it: sharpen role prompts, reduce overlap, and add review criteria that penalize redundancy.

Production recommendation: measure marginal value added per agent, not just final fluency.

## 19. Context Contamination Between Agents

What happens: one agent's assumptions bleed into another agent's role, causing confirmation bias and loss of independence.

Why it happens: all agents receive the same bloated state and message history.

How to detect it: reviewer echoes the writer, or supposedly independent agents make the same unsupported claims.

How to fix it: scope context per role and pass only the fields each agent actually needs.

Production recommendation: independence is a design property, not a prompt label.

## 20. No Production Logging

What happens: runs cannot be audited for compliance, incident review, or cost analysis.

Why it happens: teams assume tracing tools alone are enough and neglect durable operational logs.

How to detect it: you can see a live trace but cannot answer historical questions about who approved what, which model ran, or what tool payload was used.

How to fix it: persist operational metadata, route decisions, approvals, failures, and cost records in a queryable store.

Production recommendation: combine tracing for debugging with logging for audit and operations.

## Final Production Guidance

Most of these blockers share one root cause: the team treated the graph as a demo abstraction instead of a production workflow. Real systems need bounded control, durable state, explicit failure handling, path-level evaluation, and operational visibility. LangGraph can support that discipline, but it does not remove the need for it.