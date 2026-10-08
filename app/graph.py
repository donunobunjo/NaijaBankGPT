from langgraph.graph import StateGraph, START, END

from .state import AgentState


def initialize_node(state: AgentState) -> AgentState:
    """Initialize the agent state."""

    print("Initializing NaijaBankGPT...")

    return {
        **state,
        "error": None,
    }


def graph_test_node(state: AgentState) -> AgentState:
    """Temporary node used to verify that LangGraph works."""

    print("Query received:", state["user_query"])

    return {
        **state,
        "banking_reason": "Graph is working correctly.",
    }


def build_graph():
    """Build and compile the LangGraph workflow."""

    builder = StateGraph(AgentState)

    builder.add_node("initialize", initialize_node)
    builder.add_node("graph_test", graph_test_node)

    builder.add_edge(START, "initialize")
    builder.add_edge("initialize", "graph_test")
    builder.add_edge("graph_test", END)

    return builder.compile()


graph = build_graph()