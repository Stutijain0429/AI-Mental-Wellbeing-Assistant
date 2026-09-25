from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    PROJECT_ROOT
    / "notebooks"
    / "models"
    / "text_emotion_model_fast"
    / "final"
)


class TextEmotionModel:

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(str(MODEL_PATH))
        self.model = AutoModelForSequenceClassification.from_pretrained(
            str(MODEL_PATH)
        )
        self.model.eval()

    def predict(self, text):

        if not text or not text.strip():
            return None

        text_lower = text.lower()

        # Simple fallback for obvious LOVE expressions
        love_keywords = [
            "i love",
            "i loved",
            "love my",
            "love you",
            "love her",
            "love him",
            "love them",
            "feel loved",
            "feeling loved",
        ]

        # Simple fallback for obvious SURPRISE expressions
        surprise_keywords = [
            "wow",
            "cannot believe",
            "can't believe",
            "never expected",
            "unexpected",
            "what a surprise",
            "so surprised",
            "shocked",
            "i was shocked",
        ]

        if any(keyword in text_lower for keyword in love_keywords):
            return {
                "emotion": "love",
                "confidence": 0.95,
            }

        if any(keyword in text_lower for keyword in surprise_keywords):
            return {
                "emotion": "surprise",
                "confidence": 0.95,
            }

        # AI model prediction for everything else
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128,
        )

        with torch.no_grad():
            outputs = self.model(**inputs)

        probabilities = torch.softmax(outputs.logits, dim=-1)

        predicted_id = torch.argmax(
            probabilities,
            dim=-1
        ).item()

        confidence = probabilities[0][predicted_id].item()

        label = self.model.config.id2label.get(
            predicted_id,
            str(predicted_id)
        )

        return {
            "emotion": label,
            "confidence": confidence,
        }