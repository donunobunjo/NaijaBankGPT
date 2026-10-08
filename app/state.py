from typing import TypedDict, Optional


class AgentState(TypedDict, total=False):
    user_query: str
    selected_language: str
    detected_language: str

    # Banking routing
    is_banking: bool
    banking_reason: str

    # Intent classification
    intent: str
    intent_confidence: float

    # Confidence handling
    needs_clarification: bool
    clarification_question: str

    # LLM processing
    english_query: str
    llm_response: str

    # Final response
    final_response: str

    # Error handling
    error: Optional[str]