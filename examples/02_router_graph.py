from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class RouterState(TypedDict, total=False):
    query: str
    route: Literal["research", "coding", "general"]
    result: str


def route_query(state: RouterState) -> RouterState:
    """Classify the query so the graph can choose the next node."""
    query = state["query"].lower()

    if any(word in query for word in ["research", "paper", "compare", "study"]):
        route: Literal["research", "coding", "general"] = "research"
    elif any(word in query for word in ["code", "bug", "python", "function", "build"]):
        route = "coding"
    else:
        route = "general"

    return {"route": route}


def choose_next_node(state: RouterState) -> Literal["research_node", "coding_node", "general_node"]:
    route = state.get("route", "general")
    if route == "research":
        return "research_node"
    if route == "coding":
        return "coding_node"
    return "general_node"


def research_node(state: RouterState) -> RouterState:
    return {
        "result": (
            "Research path selected. In a production system, this node could perform "
            f"retrieval, evidence ranking, and synthesis for: {state['query']}"
        )
    }


def coding_node(state: RouterState) -> RouterState:
    return {
        "result": (
            "Coding path selected. In a production system, this node could inspect "
            f"files, propose edits, and run checks for: {state['query']}"
        )
    }


def general_node(state: RouterState) -> RouterState:
    return {
        "result": (
            "General path selected. In a production system, this node could provide a "
            f"direct answer or ask a clarifying question for: {state['query']}"
        )
    }


def build_graph():
    builder = StateGraph(RouterState)
    builder.add_node("route_query", route_query)
    builder.add_node("research_node", research_node)
    builder.add_node("coding_node", coding_node)
    builder.add_node("general_node", general_node)

    builder.add_edge(START, "route_query")
    builder.add_conditional_edges("route_query", choose_next_node)
    builder.add_edge("research_node", END)
    builder.add_edge("coding_node", END)
    builder.add_edge("general_node", END)

    return builder.compile()


if __name__ == "__main__":
    graph = build_graph()

    for sample_query in [
        "Compare recent research on retrieval evaluation",
        "Build a Python function to parse CSV input",
        "What is LangGraph in simple terms?",
    ]:
        result = graph.invoke({"query": sample_query})
        print(f"Query: {sample_query}")
        print(f"Route: {result['route']}")
        print(f"Result: {result['result']}")
        print("-" * 80)