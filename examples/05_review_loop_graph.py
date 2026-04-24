from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class ReviewState(TypedDict, total=False):
    topic: str
    draft: str
    review_feedback: str
    approved: bool
    revision_count: int
    final_answer: str


REVISION_STEPS = [
    " Add that state is the shared data carried through the workflow.",
    " Add that nodes are workers that read and update state.",
    " Add that edges control transitions and observability helps inspect the path.",
]


def draft_node(state: ReviewState) -> ReviewState:
    """Start with a deliberately incomplete draft so the loop has work to do."""
    return {
        "draft": f"LangGraph helps orchestrate AI workflows for the topic: {state['topic']}",
        "revision_count": 0,
    }


def review_node(state: ReviewState) -> ReviewState:
    draft = state["draft"].lower()
    missing = [term for term in ["state", "nodes", "edges"] if term not in draft]

    if not missing:
        return {
            "approved": True,
            "review_feedback": "Approved. The draft covers state, nodes, and edges clearly.",
        }

    return {
        "approved": False,
        "review_feedback": f"Rejected. The draft still needs: {', '.join(missing)}.",
    }


def route_after_review(state: ReviewState) -> Literal["final_node", "revise_node"]:
    if state.get("approved") or state.get("revision_count", 0) >= 3:
        return "final_node"
    return "revise_node"


def revise_node(state: ReviewState) -> ReviewState:
    """Add one missing teaching point per loop and stop after three revisions."""
    revision_count = state.get("revision_count", 0) + 1
    addition = REVISION_STEPS[min(revision_count - 1, len(REVISION_STEPS) - 1)]
    revised_draft = state["draft"] + addition

    return {
        "draft": revised_draft,
        "revision_count": revision_count,
    }


def final_node(state: ReviewState) -> ReviewState:
    final_answer = state["draft"]
    if not state.get("approved"):
        final_answer += "\n\nNote: max review loops reached, so this is a bounded best-effort draft."

    return {"final_answer": final_answer}


def build_graph():
    builder = StateGraph(ReviewState)
    builder.add_node("draft_node", draft_node)
    builder.add_node("review_node", review_node)
    builder.add_node("revise_node", revise_node)
    builder.add_node("final_node", final_node)

    builder.add_edge(START, "draft_node")
    builder.add_edge("draft_node", "review_node")
    builder.add_conditional_edges("review_node", route_after_review)
    builder.add_edge("revise_node", "review_node")
    builder.add_edge("final_node", END)

    return builder.compile()


if __name__ == "__main__":
    graph = build_graph()
    result = graph.invoke({"topic": "LangGraph basics"})

    print("Review feedback:")
    print(result["review_feedback"])
    print("\nFinal answer:")
    print(result["final_answer"])