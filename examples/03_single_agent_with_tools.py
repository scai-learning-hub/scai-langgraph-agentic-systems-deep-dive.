import ast
import operator
import re
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class ToolState(TypedDict, total=False):
    query: str
    needs_tool: bool
    selected_tool: Literal["calculator", "documentation_lookup", "none"]
    tool_input: str
    tool_output: str
    final_answer: str
    iteration_count: int


ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def extract_expression(query: str) -> str | None:
    """Pull a simple arithmetic expression out of natural language."""
    match = re.search(r"([0-9\s\+\-\*\/\(\)\.]+)", query)
    if not match:
        return None

    expression = match.group(1).strip()
    return expression or None


def safe_eval_expression(expression: str) -> float:
    """Evaluate arithmetic without exposing the Python runtime."""
    node = ast.parse(expression, mode="eval").body

    def _eval(current_node):
        if isinstance(current_node, ast.Constant) and isinstance(current_node.value, (int, float)):
            return float(current_node.value)
        if isinstance(current_node, ast.BinOp) and type(current_node.op) in ALLOWED_OPERATORS:
            left = _eval(current_node.left)
            right = _eval(current_node.right)
            return ALLOWED_OPERATORS[type(current_node.op)](left, right)
        if isinstance(current_node, ast.UnaryOp) and type(current_node.op) in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[type(current_node.op)](_eval(current_node.operand))
        raise ValueError("Unsupported expression for calculator_tool.")

    return _eval(node)


def calculator_tool(expression: str) -> str:
    value = safe_eval_expression(expression)
    return f"calculator_tool -> {expression} = {value}"


def documentation_lookup_tool(topic: str) -> str:
    """A fake deterministic documentation lookup for teaching purposes."""
    docs = {
        "langgraph": "LangGraph is a stateful orchestration framework for nodes, edges, routing, and durable workflows.",
        "checkpoint": "Checkpointing stores workflow progress so long-running or interrupted graphs can resume safely.",
        "supervisor": "A supervisor pattern uses one controller to delegate work to specialist agents and decide when to finish.",
        "router": "A router pattern uses deterministic or model-assisted logic to select the next branch of execution.",
    }

    lowered = topic.lower()
    for key, value in docs.items():
        if key in lowered:
            return f"documentation_lookup_tool -> {value}"

    return "documentation_lookup_tool -> No exact documentation snippet found."


def agent_node(state: ToolState) -> ToolState:
    """Decide whether to answer directly or request a deterministic tool."""
    query = state["query"]
    iteration_count = state.get("iteration_count", 0) + 1
    tool_output = state.get("tool_output")

    if tool_output:
        return {
            "needs_tool": False,
            "selected_tool": "none",
            "final_answer": (
                "The agent used a deterministic tool because the query needed external "
                f"support. Tool result: {tool_output}"
            ),
            "iteration_count": iteration_count,
        }

    expression = extract_expression(query)
    if expression and any(symbol in expression for symbol in ["+", "-", "*", "/"]):
        return {
            "needs_tool": True,
            "selected_tool": "calculator",
            "tool_input": expression,
            "iteration_count": iteration_count,
        }

    if any(word in query.lower() for word in ["langgraph", "checkpoint", "supervisor", "router"]):
        return {
            "needs_tool": True,
            "selected_tool": "documentation_lookup",
            "tool_input": query,
            "iteration_count": iteration_count,
        }

    return {
        "needs_tool": False,
        "selected_tool": "none",
        "final_answer": (
            "The agent answered directly because the request did not need a tool. In "
            f"production, this policy keeps latency and cost lower: {query}"
        ),
        "iteration_count": iteration_count,
    }


def tool_node(state: ToolState) -> ToolState:
    """Execute the selected deterministic tool."""
    selected_tool = state.get("selected_tool", "none")
    tool_input = state.get("tool_input", "")

    if selected_tool == "calculator":
        tool_output = calculator_tool(tool_input)
    elif selected_tool == "documentation_lookup":
        tool_output = documentation_lookup_tool(tool_input)
    else:
        tool_output = "No tool executed."

    return {
        "tool_output": tool_output,
        "needs_tool": False,
    }


def route_after_agent(state: ToolState) -> Literal["tool_node", "end"]:
    if state.get("needs_tool"):
        return "tool_node"
    return "end"


def build_graph():
    builder = StateGraph(ToolState)
    builder.add_node("agent_node", agent_node)
    builder.add_node("tool_node", tool_node)

    builder.add_edge(START, "agent_node")
    builder.add_conditional_edges(
        "agent_node",
        route_after_agent,
        {"tool_node": "tool_node", "end": END},
    )
    builder.add_edge("tool_node", "agent_node")

    return builder.compile()


if __name__ == "__main__":
    graph = build_graph()

    for sample_query in [
        "What is LangGraph checkpointing?",
        "Please calculate 12 * (3 + 4)",
        "Explain why deterministic tools are useful",
    ]:
        result = graph.invoke({"query": sample_query})
        print(f"Query: {sample_query}")
        print(f"Iterations: {result['iteration_count']}")
        print(f"Final answer: {result['final_answer']}")
        print("-" * 80)