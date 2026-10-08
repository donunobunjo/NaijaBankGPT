from app.state import AgentState


class TranslationService:
    """
    Translation service for Nigerian languages.

    N-ATLaS integration will be connected here.
    """

    SUPPORTED_LANGUAGES = {
        "English": "English",
        "Yoruba": "Yoruba",
        "Hausa": "Hausa",
        "Igbo": "Igbo",
    }

    def __init__(self):
        print("Initializing translation service...")

    def translate_to_english(
        self,
        text: str,
        language: str,
    ) -> str:
        """
        Translate user text into English.

        English requires no translation.
        """

        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        if language == "English":
            return text

        if language not in self.SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language: {language}"
            )

        # N-ATLaS will be connected here.
        raise NotImplementedError(
            "N-ATLaS translation has not been connected yet."
        )

    def translate_from_english(
        self,
        text: str,
        language: str,
    ) -> str:
        """
        Translate an English response into the
        user's selected language.
        """

        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        if language == "English":
            return text

        if language not in self.SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language: {language}"
            )

        # N-ATLaS will be connected here.
        raise NotImplementedError(
            "N-ATLaS translation has not been connected yet."
        )


def translate_to_english_node(
    state: AgentState,
) -> AgentState:
    """
    LangGraph node that prepares the user's query
    for the English reasoning model.
    """

    query = state["user_query"]
    language = state["selected_language"]

    print(
        f"Preparing translation: "
        f"{language} → English"
    )

    # Get the shared translation service.
    translation_service = TranslationService()

    english_query = translation_service.translate_to_english(
        text=query,
        language=language,
    )

    print(f"English query: {english_query}")

    return {
        **state,
        "english_query": english_query,
    }