"""
J.A.R.V.I.S. Embedding Classifier
Classification using pre-computed intent embeddings.
"""

from typing import List, Tuple, Dict, Optional

from jarvis_core.logger import Logger


class EmbeddingClassifier:
    def __init__(self):
        self.log = Logger("EmbeddingClassifier")
        self._model = None
        self._intent_embeddings: Dict[str, List[float]] = {}
        self._initialized = False

    def initialize(self) -> bool:
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer("all-MiniLM-L6-v2")
            self._compute_intent_embeddings()
            self._initialized = True
            self.log.info("Embedding classifier ready.")
            return True
        except ImportError:
            self.log.warn("sentence-transformers not installed.")
            self._initialized = True
            return True
        except Exception as e:
            self.log.warn(f"Embedding classifier init failed: {e}")
            self._initialized = True
            return True

    def _compute_intent_embeddings(self) -> None:
        if self._model is None:
            return

        intent_descriptions = {
            "search": "Search the web for information and facts",
            "news": "Get current news headlines and stories",
            "weather": "Check weather conditions and forecasts",
            "map": "Show maps and find locations",
            "system": "Control the computer and applications",
            "camera": "Open or control the camera",
            "music": "Play music and control playback",
            "conversation": "General conversation and chat",
        }

        for intent, description in intent_descriptions.items():
            embedding = self._model.encode([description])[0]
            self._intent_embeddings[intent] = embedding.tolist()

    def classify(self, text: str) -> Tuple[str, float]:
        if self._model is None or not self._intent_embeddings:
            return "conversation", 0.0

        try:
            import numpy as np
            text_embedding = self._model.encode([text])[0]

            best_intent = "conversation"
            best_similarity = -1.0

            for intent, intent_emb in self._intent_embeddings.items():
                similarity = np.dot(text_embedding, intent_emb)
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_intent = intent

            confidence = max(0.0, min(1.0, (best_similarity + 0.5)))
            return best_intent, confidence

        except Exception as e:
            self.log.error(f"Embedding classification failed: {e}")
            return "conversation", 0.0

    def add_custom_intent(self, intent: str, description: str) -> None:
        if self._model is not None:
            embedding = self._model.encode([description])[0]
            self._intent_embeddings[intent] = embedding.tolist()