from __future__ import annotations

from functools import lru_cache
from operator import add
from typing import Annotated, Literal, TypedDict
from uuid import uuid4

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph

from deployment.app.config import get_settings


class WorkflowState(TypedDict, total=False):
    user_query: str
    research_notes: str
    design_notes: str
    review_decision: Literal["pending", "approved", "revise_research", "revise_design"]
    review_feedback: str
    next_step: Literal["research_agent", "lab_designer_agent", "reviewer_agent", "final_agent"]
    iteration_count: int
    max_iterations: int
    final_answer: str
    trace: Annotated[list[str], add]


@lru_cache(maxsize=1)
def get_llm() -> ChatGroq:
    settings = get_settings()
    return ChatGroq(
        model=settings.model_name,
        temperature=0.2,
        groq_api_key=settings.groq_api_key,
    )


def invoke_llm(system_prompt: str, user_prompt: str) -> str:
    response = get_llm().invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
    )
    content = response.content
    if isinstance(content, str):
        return content.strip()
    return str(content).strip()


def supervisor_agent(state: WorkflowState) -> WorkflowState:
    iteration_count = state.get("iteration_count", 0)
    max_iterations = state.get("max_iterations", get_settings().max_iterations)
    review_decision = state.get("review_decision", "pending")

    if iteration_count >= max_iterations:
        return {
            "next_step": "final_agent",
            "trace": [f"Supervisor stopped further delegation at max_iterations={max_iterations}."],
        }

    if not state.get("research_notes"):
        return {"next_step": "research_agent", "trace": ["Supervisor routed to research_agent."]}

    if not state.get("design_notes"):
        return {
            "next_step": "lab_designer_agent",
            "trace": ["Supervisor routed to lab_designer_agent."],
        }

    if review_decision == "revise_research":
        return {"next_step": "research_agent", "trace": ["Supervisor requested a research revision."]}

    if review_decision == "revise_design":
        return {
            "next_step": "lab_designer_agent",
            "trace": ["Supervisor requested a design revision."],
        }

    if review_decision == "approved":
        return {"next_step": "final_agent", "trace": ["Supervisor routed to final_agent."]}

    return {"next_step": "reviewer_agent", "trace": ["Supervisor routed to reviewer_agent."]}


def route_from_supervisor(
    state: WorkflowState,
) -> Literal["research_agent", "lab_designer_agent", "reviewer_agent", "final_agent"]:
    return state["next_step"]


def research_agent(state: WorkflowState) -> WorkflowState:
    prompt = f"""
User request:
{state['user_query']}

Reviewer feedback:
{state.get('review_feedback', 'None')}

Write concise research notes with:
1. Problem framing
2. Key constraints
3. Important system considerations
4. Production risks
""".strip()

    notes = invoke_llm(
        "You are a research agent for production AI systems. Be technical and practical.",
        prompt,
    )
    return {
        "research_notes": notes,
        "review_decision": "pending",
        "iteration_count": state.get("iteration_count", 0) + 1,
        "trace": ["research_agent updated research_notes."],
    }


def lab_designer_agent(state: WorkflowState) -> WorkflowState:
    prompt = f"""
User request:
{state['user_query']}

Research notes:
{state.get('research_notes', 'Missing')}

Reviewer feedback:
{state.get('review_feedback', 'None')}

Create a design with:
1. Workflow steps
2. State fields
3. Deployment considerations
4. Validation and reliability notes
""".strip()

    design_notes = invoke_llm(
        "You are a lab designer agent. Turn research into a concrete agent workflow design.",
        prompt,
    )
    return {
        "design_notes": design_notes,
        "review_decision": "pending",
        "iteration_count": state.get("iteration_count", 0) + 1,
        "trace": ["lab_designer_agent updated design_notes."],
    }


def parse_review_decision(review_text: str) -> Literal["approved", "revise_research", "revise_design"]:
    first_line = review_text.splitlines()[0].strip().upper() if review_text.strip() else ""

    if first_line == "APPROVED":
        return "approved"
    if first_line == "REVISE_RESEARCH":
        return "revise_research"
    if first_line == "REVISE_DESIGN":
        return "revise_design"
    if "REVISE_RESEARCH" in review_text.upper():
        return "revise_research"
    if "REVISE_DESIGN" in review_text.upper():
        return "revise_design"
    return "approved"


def reviewer_agent(state: WorkflowState) -> WorkflowState:
    prompt = f"""
User request:
{state['user_query']}

Research notes:
{state.get('research_notes', 'Missing')}

Design notes:
{state.get('design_notes', 'Missing')}

Return exactly one token on the first line:
APPROVED
REVISE_RESEARCH
REVISE_DESIGN

Then add a brief explanation.
""".strip()

    review_text = invoke_llm(
        "You are a reviewer agent. Check completeness, realism, and production quality.",
        prompt,
    )
    decision = parse_review_decision(review_text)
    feedback = "\n".join(review_text.splitlines()[1:]).strip() or review_text
    return {
        "review_decision": decision,
        "review_feedback": feedback,
        "trace": [f"reviewer_agent returned {decision}."],
    }


def final_agent(state: WorkflowState) -> WorkflowState:
    prompt = f"""
User request:
{state['user_query']}

Research notes:
{state.get('research_notes', 'Missing')}

Design notes:
{state.get('design_notes', 'Missing')}

Review decision:
{state.get('review_decision', 'pending')}

Review feedback:
{state.get('review_feedback', 'None')}

Write a final answer with practical steps, reliability notes, and production trade-offs.
If iteration limits were hit, say that the result is bounded by the configured workflow budget.
""".strip()

    final_answer = invoke_llm(
        "You are the final agent. Produce a concise but production-grade final response.",
        prompt,
    )
    return {
        "final_answer": final_answer,
        "trace": ["final_agent produced the final answer."],
    }


@lru_cache(maxsize=1)
def build_graph():
    builder = StateGraph(WorkflowState)
    builder.add_node("supervisor_agent", supervisor_agent)
    builder.add_node("research_agent", research_agent)
    builder.add_node("lab_designer_agent", lab_designer_agent)
    builder.add_node("reviewer_agent", reviewer_agent)
    builder.add_node("final_agent", final_agent)

    builder.add_edge(START, "supervisor_agent")
    builder.add_conditional_edges(
        "supervisor_agent",
        route_from_supervisor,
        {
            "research_agent": "research_agent",
            "lab_designer_agent": "lab_designer_agent",
            "reviewer_agent": "reviewer_agent",
            "final_agent": "final_agent",
        },
    )
    builder.add_edge("research_agent", "supervisor_agent")
    builder.add_edge("lab_designer_agent", "supervisor_agent")
    builder.add_edge("reviewer_agent", "supervisor_agent")
    builder.add_edge("final_agent", END)
    return builder.compile()


def run_graph(user_query: str) -> dict[str, object]:
    settings = get_settings()
    app = build_graph()
    result = app.invoke(
        {
            "user_query": user_query,
            "iteration_count": 0,
            "max_iterations": settings.max_iterations,
            "review_decision": "pending",
            "trace": [],
        }
    )

    return {
        "request_id": str(uuid4()),
        "status": "completed",
        "environment": settings.environment,
        "model_name": settings.model_name,
        "max_iterations": settings.max_iterations,
        "iterations_used": result.get("iteration_count", 0),
        "review_decision": result.get("review_decision", "pending"),
        "answer": result.get("final_answer", ""),
        "trace": result.get("trace", []),
    }
