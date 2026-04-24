from operator import add
from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph


class CheckpointState(TypedDict, total=False):
    query: str
    notes: Annotated[list[str], add]
    final_answer: str


def analyze_request(state: CheckpointState) -> CheckpointState:
    """Capture durable notes so the workflow can resume with context."""
    return {
        "notes": [
            f"Captured query: {state['query']}",
            "Marked the workflow as something that should be resumable.",
        ]
    }


def answer_request(state: CheckpointState) -> CheckpointState:
    answer = (
        "Checkpointing matters because long-running graphs may pause for tool retries, "
        "human approval, or external system failures. Saving state lets the workflow "
        "resume without starting from scratch."
    )
    return {
        "final_answer": answer,
        "notes": ["Built the final answer from the checkpointed state."],
    }


def build_graph():
    # MemorySaver is useful for local learning and debugging.
    # Production systems should replace it with a persistent checkpoint store.
    checkpointer = MemorySaver()

    builder = StateGraph(CheckpointState)
    builder.add_node("analyze_request", analyze_request)
    builder.add_node("answer_request", answer_request)

    builder.add_edge(START, "analyze_request")
    builder.add_edge("analyze_request", "answer_request")
    builder.add_edge("answer_request", END)

    return builder.compile(checkpointer=checkpointer)


if __name__ == "__main__":
    graph = build_graph()
    config = {"configurable": {"thread_id": "checkpoint-demo-1"}}

    result = graph.invoke(
        {"query": "Why does checkpointing matter for human approval workflows?"},
        config=config,
    )
    snapshot = graph.get_state(config)

    print("Final state:")
    print(result)
    print("\nCheckpointed values:")
    print(snapshot.values)
    print("\nProduction note:")
    print("MemorySaver is for local development. Use a persistent checkpoint backend in production.")