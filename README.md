<div align="center">

# 🧠 LangGraph: Agentic Systems Deep Dive

### From Developer Basics to Research & Architect-Level Multi-Agent Systems

<br/>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2%2B-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://github.com/langchain-ai/langgraph)
[![LangChain](https://img.shields.io/badge/LangChain-0.3%2B-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://github.com/langchain-ai/langchain)
[![FastAPI](https://img.shields.io/badge/FastAPI-Production%20Ready-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Stars](https://img.shields.io/github/stars/scai-learning-hub/scai-langgraph-agentic-systems-deep-dive?style=for-the-badge&color=yellow)](https://github.com/scai-learning-hub/scai-langgraph-agentic-systems-deep-dive/stargazers)

<br/>

> **LangGraph is not just another agent framework.**
> It is a stateful, graph-based orchestration system for building controlled, durable, inspectable, and production-ready agent workflows.
> This repo teaches LangGraph the way working engineers actually need it.

<br/>

[🚀 Quick Start](#-quick-start) · [📚 Learning Paths](#-learning-paths) · [🗂 Structure](#-repository-structure) · [🧩 Examples](#-examples) · [🏭 Deployment](#-deployment) · [🎓 Courses](#-learn-more-with-school-of-core-ai)

</div>

---

## 📌 What Is This Repository?

Most LangGraph tutorials show you syntax. This repo shows you **thinking**.

You will learn:

- ✅ Why LangGraph exists and when you actually need it
- ✅ How to design state schemas that survive production traffic
- ✅ How to build nodes, edges, reducers, and conditional routes
- ✅ How to implement single-agent, supervisor, and review-loop patterns
- ✅ How to reason about checkpointing, memory, retries, and observability
- ✅ Where multi-agent systems help — and where they add unnecessary complexity

---

## 👥 Who This Is For

| Audience | Focus |
|---|---|
| **1–3 yr developers** | Mental models, state flow, runnable code, basic routing |
| **3–7 yr engineers** | Tool use, retries, review loops, testable workflows |
| **7–12 yr senior engineers** | State design, observability, evaluation, fault tolerance |
| **12–20 yr architects** | System trade-offs, governance, long-horizon agent design |

---

## 📚 Learning Paths

<details>
<summary><strong>🟢 1–3 Years — Start Here</strong></summary>

<br/>

1. `01-why-langgraph.md`
2. `02-langgraph-core-concepts.md`
3. `examples/01_basic_graph.py`
4. `examples/02_router_graph.py`
5. `04-single-agent-workflow.md`

> Focus on how state moves, why graphs beat ad hoc `if/else` chains, and how routing changes control flow.

</details>

<details>
<summary><strong>🔵 3–7 Years — Focus Here</strong></summary>

<br/>

1. `03-state-nodes-edges-routing.md`
2. `04-single-agent-workflow.md`
3. `05-multi-agent-supervisor-pattern.md`
4. `examples/03_single_agent_with_tools.py`
5. `examples/05_review_loop_graph.py`

> Focus on tool boundaries, retries, review loops, and keeping workflows observable and testable.

</details>

<details>
<summary><strong>🟠 7–12 Years — Architecture Path</strong></summary>

<br/>

1. `06-production-blockers-and-failure-modes.md`
2. `07-architectural-patterns.md`
3. `examples/04_multi_agent_supervisor.py`
4. `examples/06_checkpointing_example.py`

> Focus on state schema design, supervisor bottlenecks, human approval gates, and deployment strategy.

</details>

<details>
<summary><strong>🔴 12–20 Years — Research & System Design</strong></summary>

<br/>

1. `07-architectural-patterns.md`
2. `08-research-level-directions.md`
3. `09-interview-and-discussion-questions.md`

> Focus on agent communication protocols, planning vs execution, memory compression, cost-aware routing, and governance.

</details>

---

## 🗂 Repository Structure

```
scai-langgraph-agentic-systems-deep-dive/
│
├── 📄 README.md
│
├── 📚 Guides (read in order)
│   ├── 01-why-langgraph.md
│   ├── 02-langgraph-core-concepts.md
│   ├── 03-state-nodes-edges-routing.md
│   ├── 04-single-agent-workflow.md
│   ├── 05-multi-agent-supervisor-pattern.md
│   ├── 06-production-blockers-and-failure-modes.md
│   ├── 07-architectural-patterns.md
│   ├── 08-research-level-directions.md
│   ├── 09-interview-and-discussion-questions.md
│   └── 10-deployment-and-productionization.md
│
├── 🧩 examples/
│   ├── 01_basic_graph.py
│   ├── 02_router_graph.py
│   ├── 03_single_agent_with_tools.py
│   ├── 04_multi_agent_supervisor.py
│   ├── 05_review_loop_graph.py
│   └── 06_checkpointing_example.py
│
├── 🏭 deployment/
│   ├── app/
│   │   ├── api.py              ← FastAPI endpoints
│   │   ├── graph_service.py    ← Graph runner
│   │   └── config.py          ← Pydantic settings
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── local_run.md
│   ├── docker.md
│   ├── fastapi_service.md
│   ├── env_config.md
│   ├── observability.md
│   └── deployment_checklist.md
│
├── 📊 diagrams/
│   ├── langgraph-basic-flow.md
│   ├── supervisor-pattern-flow.md
│   └── production-architecture-flow.md
│
└── 📦 requirements.txt
```

---

## 🚀 Quick Start

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/scai-learning-hub/scai-langgraph-agentic-systems-deep-dive.
cd scai-langgraph-agentic-systems-deep-dive.
python -m venv .venv
```

### 2. Install Dependencies

```bash
# Windows
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Set Your API Key

```bash
# Windows PowerShell
$env:GROQ_API_KEY="your_groq_api_key_here"

# macOS / Linux
export GROQ_API_KEY=your_groq_api_key_here
```

> Get your free Groq API key at [console.groq.com](https://console.groq.com)

### 4. Run Your First Example

```bash
python examples/01_basic_graph.py
```

**Expected Output:**
```text
Final state:
{'query': 'How does LangGraph help with retries?', 'query_type': 'question',
 'answer': 'This looks like an explanatory question...'}

Final answer:
This looks like an explanatory question. In production, this node could
route to a knowledge or retrieval layer before answering.
```

---

## 🧩 Examples

| File | What It Demonstrates |
|---|---|
| `01_basic_graph.py` | State flow through a minimal 3-node graph |
| `02_router_graph.py` | Conditional routing based on query classification |
| `03_single_agent_with_tools.py` | Tool-calling agent with bounded iteration |
| `04_multi_agent_supervisor.py` | Supervisor delegating to specialized sub-agents |
| `05_review_loop_graph.py` | Human-in-the-loop review before continuation |
| `06_checkpointing_example.py` | Durable state with checkpoint resume |

---

## 🏭 Deployment

This repo includes a **production-ready FastAPI service** with Docker support.

```bash
cd deployment

# Run locally
uvicorn app.api:app --reload

# Run with Docker
docker-compose up --build
```

**API Endpoints:**

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/invoke` | Run graph with a user query |

See [`deployment/`](deployment/) for full docs on local run, Docker, env config, observability, and deployment checklist.

---

## 🧠 LangGraph Mental Models

> These 10 analogies help engineers reason about the system before reading a single line of code.

| Concept | Mental Model |
|---|---|
| **State** | The shared whiteboard everyone reads and writes |
| **Nodes** | Workers who do one job at a time |
| **Edges** | Roads between workers |
| **Conditional Edges** | Traffic signals that decide which road to take |
| **Reducers** | Rules for merging updates from multiple nodes |
| **Checkpoints** | Saved game states — resume from any point |
| **Supervisor** | The project manager who delegates work |
| **Tools** | External abilities the agent can call |
| **Observability** | The CCTV system of your workflow |
| **Evaluation** | The quality gate before you ship |

---

## 📊 What Each Experience Level Should Take Away

| Experience | What They Usually See | What LangGraph Teaches Them |
|---|---|---|
| **1-year developer** | Nodes and edges as simple functions | How state moves, why control flow is a first-class design problem |
| **5-year engineer** | Agent workflow and tool use | Routing, retries, review loops, and explicit failure handling |
| **10-year senior** | Orchestration and production reliability | State design, observability, evaluation, bounded autonomy |
| **20-year architect** | Distributed system trade-offs | Durability, governance, memory architecture, long-horizon agent design |

---

## 💡 Why This Matters In Real Systems

An LLM call by itself is not a system.

The system is the **workflow around the model**: what state is kept, how failure is handled, which tool calls are trusted, how retries are bounded, who approves risky actions, and how performance is measured.

LangGraph matters because it forces those workflow decisions **into code** — rather than leaving them as implicit prompt behavior.

---

## 🎓 Learn More With School of Core AI

<div align="center">

> **Want structured, mentor-led training to build production AI systems?**

| Course | Who It's For | Link |
|---|---|---|
| 🧑‍💻 **AI Developer Course** | Build AI apps with APIs, FastAPI, RAG, evaluation, and product implementation | [View Course →](https://schoolofcoreai.com/courses/ai-developers-course) |
| 🤖 **Agentic AI Course** | LangGraph, multi-agent orchestration, AgentOps, tracing, guardrails, MCP, production deployment | [View Course →](https://schoolofcoreai.com/courses/agentic-ai-course) |

[🌐 Visit School of Core AI](https://schoolofcoreai.com/)

</div>

---

## ✅ Suggested Next Steps

1. **Run** `examples/01_basic_graph.py` and `examples/02_router_graph.py` to understand state flow
2. **Read** `06-production-blockers-and-failure-modes.md` before building anything customer-facing
3. **Read** `10-deployment-and-productionization.md` before turning the workflow into an API
4. **Adapt** `examples/05_review_loop_graph.py` and `examples/06_checkpointing_example.py` before adding human approval or persistence to a real service

---

<div align="center">

**Built with ❤️ by [School of Core AI](https://schoolofcoreai.com/)**

*If this repo helped you, consider giving it a ⭐ — it helps more engineers find it.*

</div>