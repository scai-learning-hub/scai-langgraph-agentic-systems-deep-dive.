from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class GraphState(TypedDict, total=False):
    query: str
    query_type: Literal["question", "task", "unknown"]
    answer: str


def classify_query(state: GraphState) -> GraphState:
    """Classify the user request so later nodes can stay simple."""
    query = state["query"].lower()

    if any(word in query for word in ["how", "what", "why", "when"]):
        query_type: Literal["question", "task", "unknown"] = "question"
    elif any(word in query for word in ["build", "create", "write", "design"]):
        query_type = "task"
    else:
        query_type = "unknown"

    return {"query_type": query_type}


def answer_node(state: GraphState) -> GraphState:
    """Produce a final answer from the classified state."""
    query_type = state.get("query_type", "unknown")
    query = state["query"]

    if query_type == "question":
        answer = (
            "This looks like an explanatory question. In production, this node could "
            f"route to a knowledge or retrieval layer before answering: {query}"
        )
    elif query_type == "task":
        answer = (
            "This looks like an action request. In production, this node could trigger "
            f"planning, tool use, or approval steps before execution: {query}"
        )
    else:
        answer = (
            "The query is ambiguous. In production, the graph should either ask a "
            f"clarifying question or use a safer default path: {query}"
        )

    return {"answer": answer}


def build_graph():
    builder = StateGraph(GraphState)
    builder.add_node("classify_query", classify_query)
    builder.add_node("answer_node", answer_node)

    builder.add_edge(START, "classify_query")
    builder.add_edge("classify_query", "answer_node")
    builder.add_edge("answer_node", END)

    return builder.compile()


if __name__ == "__main__":
    graph = build_graph()
    result = graph.invoke({"query": "How does LangGraph help with retries?"})

    print("Final state:")
    print(result)
    print("\nFinal answer:")
    print(result["answer"])