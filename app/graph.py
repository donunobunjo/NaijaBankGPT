from langgraph.graph import StateGraph, START, END

from .state import AgentState
from .nodes.intent import BankingIntentClassifier
from .nodes.router import banking_router

from .nodes.translation import TranslationService



from langgraph.graph import StateGraph, START, END

from .state import AgentState
from .nodes.intent import BankingIntentClassifier
from .nodes.router import banking_router
from .nodes.translation import (
    TranslationService,
    translate_to_english_node,
)




# Load the classifier once when the application starts.
intent_classifier = BankingIntentClassifier()
# translation_service = TranslationService()

def initialize_node(state: AgentState) -> AgentState:
    print("Initializing NaijaBankGPT...")

    return {
        **state,
        "error": None,
    }


def banking_router_node(state: AgentState) -> AgentState:
    """
    Determine whether the user's query is banking-related.
    """

    query = state["user_query"]

    print(f"Routing query: {query}")

    result = banking_router(query)

    print(f"Is banking: {result['is_banking']}")
    print(f"Reason: {result['banking_reason']}")

    return {
        **state,
        "is_banking": result["is_banking"],
        "banking_reason": result["banking_reason"],
    }


def route_after_banking_check(state: AgentState) -> str:
    """
    Decide which node should run next.
    """

    if state.get("is_banking", False):
        return "banking"

    return "non_banking"


CONFIDENCE_THRESHOLD = 0.60


def intent_classifier_node(state: AgentState) -> AgentState:
    """
    Classify a banking query into one of the 77 Banking77 intents.

    If confidence is below the threshold, the intent is not trusted.
    """

    query = state["user_query"]

    print(f"Classifying query: {query}")

    result = intent_classifier.predict(query)

    intent = result["intent"]
    confidence = result["confidence"]

    print(f"Intent: {intent}")
    print(f"Confidence: {confidence:.4f}")

    if confidence < CONFIDENCE_THRESHOLD:

        print(
            f"Confidence below threshold "
            f"({CONFIDENCE_THRESHOLD})."
        )

        return {
            **state,
            "intent": intent,
            "intent_confidence": confidence,
            "needs_clarification": True,
            "clarification_question": (
                "Could you provide a little more detail "
                "about the banking issue you are experiencing?"
            ),
        }

    return {
        **state,
        "intent": intent,
        "intent_confidence": confidence,
        "needs_clarification": False,
        "clarification_question": "",
    }



def clarification_node(state: AgentState) -> AgentState:
    """
    Ask the user for more information when intent confidence is low.
    """

    question = state.get(
        "clarification_question",
        "Could you provide more details about your banking issue?",
    )

    print("Clarification required.")

    return {
        **state,
        "final_response": question,
    }


def non_banking_node(state: AgentState) -> AgentState:
    """
    Temporary handler for non-banking queries.

    We will replace this with the LLM response node later.
    """

    query = state["user_query"]

    print(f"Non-banking query: {query}")

    return {
        **state,
        "final_response": (
            "This query does not appear to be banking-related."
        ),
    }


def route_after_intent_classification(
    state: AgentState,
) -> str:

    if state.get("needs_clarification", False):
        return "clarification"

    return "confident"


def build_graph():

    builder = StateGraph(AgentState)

    # Nodes
    builder.add_node(
        "initialize",
        initialize_node,
    )

    builder.add_node(
        "banking_router",
        banking_router_node,
    )

    builder.add_node(
        "intent_classifier",
        intent_classifier_node,
    )

    builder.add_node(
        "clarification",
        clarification_node,
    )

    builder.add_node(
        "non_banking",
        non_banking_node,
    )

    # START → initialize
    builder.add_edge(
        START,
        "initialize",
    )

    # initialize → banking router
    builder.add_edge(
        "initialize",
        "banking_router",
    )

    # Banking / non-banking decision
    builder.add_conditional_edges(
        "banking_router",
        route_after_banking_check,
        {
            "banking": "intent_classifier",
            "non_banking": "non_banking",
        },
    )

    # Intent confidence decision
    builder.add_conditional_edges(
        "intent_classifier",
        route_after_intent_classification,
        {
            "confident": "translate_to_english",
            "clarification": "clarification",
        },
    )

    # Clarification → END
    builder.add_edge(
        "clarification",
        END,
    )

    # Non-banking → END
    builder.add_edge(
        "non_banking",
        END,
    )

    builder.add_node(
        "translate_to_english",
        translate_to_english_node,
    )


    builder.add_edge(
        "translate_to_english",
        END,
    )
    

    return builder.compile()


graph = build_graph()