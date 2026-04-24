from __future__ import annotations

import os
from operator import add
from typing import Annotated, Literal, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph


load_dotenv()


class SupervisorState(TypedDict, total=False):
    user_query: str
    research_notes: str
    lab_plan: str
    review_decision: Literal["pending", "approved", "revise_research", "revise_design"]
    review_feedback: str
    next_step: Literal["research_agent", "lab_designer_agent", "reviewer_agent", "final_agent"]
    iteration_count: int
    max_iterations: int
    final_answer: str
    trace: Annotated[list[str], add]


_LLM: ChatGroq | None = None


def get_llm() -> ChatGroq:
    """Create the Groq client lazily so import-time setup stays lightweight."""
    global _LLM

    if _LLM is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("Set GROQ_API_KEY before running this example.")

        model_name = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        _LLM = ChatGroq(model=model_name, temperature=0.2, groq_api_key=api_key)

    return _LLM


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


def supervisor_agent(state: SupervisorState) -> SupervisorState:
    """Route work based on structured state rather than freeform history."""
    iteration_count = state.get("iteration_count", 0)
    max_iterations = state.get("max_iterations", 4)
    review_decision = state.get("review_decision", "pending")

    if iteration_count >= max_iterations:
        return {
            "next_step": "final_agent",
            "trace": [f"Supervisor forced finalization after reaching max_iterations={max_iterations}."],
        }

    if not state.get("research_notes"):
        return {"next_step": "research_agent", "trace": ["Supervisor routed to research_agent."]}

    if not state.get("lab_plan"):
        return {
            "next_step": "lab_designer_agent",
            "trace": ["Supervisor routed to lab_designer_agent."],
        }

    if review_decision == "revise_research":
        return {"next_step": "research_agent", "trace": ["Supervisor requested research revision."]}

    if review_decision == "revise_design":
        return {
            "next_step": "lab_designer_agent",
            "trace": ["Supervisor requested design revision."],
        }

    if review_decision == "approved":
        return {"next_step": "final_agent", "trace": ["Supervisor routed to final_agent."]}

    return {"next_step": "reviewer_agent", "trace": ["Supervisor routed to reviewer_agent."]}


def route_from_supervisor(
    state: SupervisorState,
) -> Literal["research_agent", "lab_designer_agent", "reviewer_agent", "final_agent"]:
    return state["next_step"]


def research_agent(state: SupervisorState) -> SupervisorState:
    """Gather conceptual grounding and constraints for the task."""
    prompt = f"""
User request:
{state['user_query']}

Reviewer feedback:
{state.get('review_feedback', 'None')}

Produce concise research notes with:
1. Problem framing
2. Key constraints
3. Useful concepts
4. Production risks
""".strip()

    notes = invoke_llm(
        "You are a research agent. Write practical engineering notes, not marketing copy.",
        prompt,
    )
    return {
        "research_notes": notes,
        "review_decision": "pending",
        "iteration_count": state.get("iteration_count", 0) + 1,
        "trace": ["research_agent updated research_notes."],
    }


def lab_designer_agent(state: SupervisorState) -> SupervisorState:
    """Turn the research into an actionable system design or experiment plan."""
    prompt = f"""
User request:
{state['user_query']}

Research notes:
{state.get('research_notes', 'No research notes yet.')}

Reviewer feedback:
{state.get('review_feedback', 'None')}

Create a practical design with:
1. Workflow steps
2. State fields
3. Tooling or infrastructure needs
4. Validation plan
""".strip()

    plan = invoke_llm(
        "You are a lab designer agent. Create clear, actionable plans for AI workflows.",
        prompt,
    )
    return {
        "lab_plan": plan,
        "review_decision": "pending",
        "iteration_count": state.get("iteration_count", 0) + 1,
        "trace": ["lab_designer_agent updated lab_plan."],
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


def reviewer_agent(state: SupervisorState) -> SupervisorState:
    """Review whether the system is complete enough to finalize."""
    prompt = f"""
User request:
{state['user_query']}

Research notes:
{state.get('research_notes', 'Missing')}

Lab plan:
{state.get('lab_plan', 'Missing')}

Return exactly one of these tokens on the first line:
APPROVED
REVISE_RESEARCH
REVISE_DESIGN

Then give a short explanation of what is missing or why it is acceptable.
""".strip()

    review_text = invoke_llm(
        "You are a reviewer agent. Be strict about completeness and production realism.",
        prompt,
    )

    decision = parse_review_decision(review_text)
    feedback_lines = review_text.splitlines()[1:]
    feedback = "\n".join(feedback_lines).strip() or review_text

    return {
        "review_decision": decision,
        "review_feedback": feedback,
        "trace": [f"reviewer_agent returned {decision}."],
    }


def final_agent(state: SupervisorState) -> SupervisorState:
    """Synthesize the final answer from the accumulated state."""
    prompt = f"""
User request:
{state['user_query']}

Research notes:
{state.get('research_notes', 'Missing')}

Lab plan:
{state.get('lab_plan', 'Missing')}

Review decision:
{state.get('review_decision', 'pending')}

Review feedback:
{state.get('review_feedback', 'None')}

Write a final response that is practical, explicit about trade-offs, and suitable for an engineering audience.
If the review was not approved, mention that the answer is best-effort due to iteration limits.
""".strip()

    final_answer = invoke_llm(
        "You are the final agent. Produce a polished answer grounded in the earlier work.",
        prompt,
    )
    return {
        "final_answer": final_answer,
        "trace": ["final_agent produced the final answer."],
    }


def build_graph():
    builder = StateGraph(SupervisorState)
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


if __name__ == "__main__":
    graph = build_graph()
    initial_state: SupervisorState = {
        "user_query": "Design a LangGraph-based AI lab assistant for course planning.",
        "iteration_count": 0,
        "max_iterations": 4,
        "review_decision": "pending",
        "trace": [],
    }

    result = graph.invoke(initial_state)
    print("Final answer:\n")
    print(result["final_answer"])
    print("\nExecution trace:")
    for item in result.get("trace", []):
        print(f"- {item}")