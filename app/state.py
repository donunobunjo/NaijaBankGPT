from typing import TypedDict, Optional


class AgentState(TypedDict, total=False):
    # Original user input
    user_query: str

    # Language selected in the UI
    selected_language: str

    # Language detected by the agent
    detected_language: str

    # Banking classification
    is_banking: bool
    banking_reason: str

    # Banking intent
    intent: str
    intent_confidence: float

    # English version used by the LLM
    english_query: str

    # LLM-generated response
    llm_response: str

    # Final response shown to the user
    final_response: str

    # Error information
    error: Optional[str]