from pathlib import Path

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
)


# Local model directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = PROJECT_ROOT / "local_model"


class BankingIntentClassifier:
    """
    NaijaMultilingualBank intent classifier.

    The model predicts one of the 77 Banking77 intents.
    """

    def __init__(self, model_dir: str | Path = MODEL_DIR):

        self.model_dir = Path(model_dir)

        print(f"Loading NaijaMultilingualBank from: {self.model_dir}")

        if not self.model_dir.exists():
            raise FileNotFoundError(
                f"Model directory not found: {self.model_dir}"
            )

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_dir
        )

        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_dir
        )

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        self.model.to(self.device)
        self.model.eval()

        print(f"Model loaded successfully on {self.device}")
        print(f"Number of intents: {self.model.config.num_labels}")

    def predict(self, text: str) -> dict:
        """
        Predict the banking intent for a user query.
        """

        if not text or not text.strip():
            raise ValueError("Query cannot be empty.")

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=128,
        )

        inputs = {
            key: value.to(self.device)
            for key, value in inputs.items()
        }

        with torch.no_grad():
            outputs = self.model(**inputs)

        probabilities = torch.softmax(
            outputs.logits,
            dim=-1
        )

        confidence, predicted_id = torch.max(
            probabilities,
            dim=-1
        )

        predicted_id = predicted_id.item()
        confidence = confidence.item()

        intent = self.model.config.id2label[predicted_id]

        return {
            "intent": intent,
            "confidence": confidence,
            "label_id": predicted_id,
        }