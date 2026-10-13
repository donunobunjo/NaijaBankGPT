# NaijaBankGPT 🇳🇬

**A multilingual AI banking assistant for Nigerian languages**\
**Status: 🚧 Work in Progress**

NaijaBankGPT is an AI-agent project designed to help users describe
common banking questions in English, Yoruba, Hausa, or Igbo and receive
useful guidance in their selected language. It combines a fine-tuned
multilingual banking-intent classifier with a translation component and
an LLM-powered response workflow.

> **Work in progress:** The intent-classification model has been
> fine-tuned and tested, and the initial LangGraph workflow is in place.
> However, the full assistant is not yet complete: N-ATLaS translation
> is not integrated, the LLM response-generation step is not connected,
> and end-to-end multilingual conversations have not yet been validated.
> The project is therefore still under active development.

## Project Goals

-   Recognize 77 common banking intents using the
    `NaijaMultilingualBank` classifier.
-   Support English, Yoruba, Hausa, and Igbo interactions.
-   Translate non-English queries into English and translate generated
    answers back into the selected language.
-   Use LangGraph to coordinate routing, intent classification,
    clarification, translation, and response generation.
-   Provide a simple chat interface with Gradio.
-   Give general banking guidance without claiming access to real bank
    accounts, balances, or transaction systems.

## How It Is Intended to Work

1.  The user enters a question and selects a language.
2.  A routing step checks whether the question appears to be
    banking-related.
3.  `NaijaMultilingualBank` predicts the banking intent and confidence.
4.  If confidence is low, the assistant asks the user to clarify.
5.  N-ATLaS translates the query into English when necessary.
6.  An LLM accessed through Groq generates a helpful response.
7.  N-ATLaS translates the answer into the selected language when
    necessary.
8.  Gradio presents the response to the user.

*Steps involving N-ATLaS and LLM response generation are planned
integrations and are not yet fully implemented.*

## Current Progress

-   [x] Fine-tuned `NaijaMultilingualBank` for 77 Banking77 intents
    across English, Yoruba, Hausa, and Igbo.
-   [x] Evaluated the classifier on a held-out test set.
-   [x] Downloaded and verified the model for local CPU inference.
-   [x] Created the initial LangGraph state, banking router,
    intent-classification node, confidence-based clarification path, and
    non-banking response.
-   [x] Added a translation-service interface to prepare for N-ATLaS
    integration.
-   [ ] Integrate and validate N-ATLaS translation.
-   [ ] Connect the LLM response-generation step through Groq.
-   [ ] Complete the end-to-end LangGraph workflow.
-   [ ] Build and test the Gradio chatbot interface.
-   [ ] Run multilingual end-to-end tests and document deployment.

## Technology Stack

-   **Language:** Python
-   **Agent orchestration:** LangGraph, LangChain
-   **Intent classification:** PyTorch, Hugging Face Transformers, XLM-R
-   **Classifier model:**
    [NaijaMultilingualBank](https://huggingface.co/Donoe/NaijaMultilingualBank)
-   **Multilingual dataset:** [Multilingual Nigerian
    Banking77](https://huggingface.co/datasets/Donoe/multilingual-nigerian-banking77)
-   **Translation (planned):**
    [NCAIR1/N-ATLaS](https://huggingface.co/NCAIR1/N-ATLaS)
-   **LLM inference (planned):** Groq API with a compatible Llama model
-   **User interface (planned):** Gradio
-   **Configuration:** python-dotenv

## Repository Structure

``` text
NaijaBankGPT/
├── app/
│   ├── nodes/
│   │   ├── intent.py
│   │   ├── router.py
│   │   └── translation.py
│   ├── graph.py
│   └── state.py
├── tests/
├── local_model/        # Downloaded model files; excluded from Git
├── gradio_app.py       # Planned/under development
├── requirements.txt
├── .env                # Local secrets; never commit
└── .gitignore
```

The structure may change as implementation progresses. Do not commit
`.env`, access tokens, or large local model files.

## Setup

### 1. Clone the repository

``` bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd NaijaBankGPT
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

``` powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

``` powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root for the API credentials needed
by integrations as they are connected. For example:

``` env
HF_TOKEN=your_hugging_face_token
GROQ_API_KEY=your_groq_api_key
```

Only add the variables you need for the feature you are testing. Keep
`.env` private and never commit real tokens.

### 5. Add the classifier model

The local development setup expects the `NaijaMultilingualBank` model
files in `local_model/`. Download the model from the [Hugging Face model
repository](https://huggingface.co/Donoe/NaijaMultilingualBank) and
place the required files there. This folder is excluded from Git because
the model weights are large.

### 6. Run the current intent test

``` powershell
python -m tests.test_intent
```

The full chatbot is not yet ready for production use. Translation, LLM
response generation, the completed Gradio interface, and end-to-end
validation remain in progress.

## Safety and Scope

NaijaBankGPT is intended to provide general information about banking
issues. It does not connect to real bank systems and cannot verify
account balances, initiate transfers, inspect private transactions, or
change account details. Users should contact their bank through official
channels for account-specific or urgent issues.

## Links

-   **Model:** [NaijaMultilingualBank on Hugging
    Face](https://huggingface.co/Donoe/NaijaMultilingualBank)
-   **Dataset:** [Multilingual Nigerian Banking77 on Hugging
    Face](https://huggingface.co/datasets/Donoe/multilingual-nigerian-banking77)
-   **Translation model:**
    [NCAIR1/N-ATLaS](https://huggingface.co/NCAIR1/N-ATLaS)
-   **GitHub:** Add repository URL after publishing
-   **Live demo:** Not available yet; planned

## Contributing

This project is actively being developed. Issues, suggestions, and
constructive feedback about multilingual coverage, intent-classification
quality, translation reliability, and user experience are welcome.

## License

Check the applicable licenses and terms for the source models, dataset,
and any deployed services before redistributing model files or using the
system commercially. In particular, review the [N-ATLaS model
terms](https://huggingface.co/NCAIR1/N-ATLaS) before integrating or
deploying it.
