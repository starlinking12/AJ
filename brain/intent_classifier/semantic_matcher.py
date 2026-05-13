"""
J.A.R.V.I.S. Semantic Matcher
Uses sentence similarity to match user input to intent examples.
"""

from typing import List, Tuple, Optional

from jarvis_core.logger import Logger
from brain.intent_classifier.intent_labels import IntentLabels


class SemanticMatcher:
    def __init__(self):
        self.log = Logger("SemanticMatcher")
        self.intent_labels = IntentLabels()
        self._model = None
        self._initialized = False
        self._embeddings = {}

    def initialize(self) -> bool:
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer("all-MiniLM-L6-v2")
            self._build_embeddings()
            self._initialized = True
            self.log.info("Semantic matcher ready.")
            return True
        except ImportError:
            self.log.warn("sentence-transformers not installed.")
            self._initialized = True
            return True
        except Exception as e:
            self.log.warn(f"Semantic matcher init failed: {e}")
            self._initialized = True
            return True

    def _build_embeddings(self) -> None:
        if self._model is None:
            return
        for intent in self.intent_labels.get_all_intents():
            examples = self.intent_labels.get_examples(intent)
            if examples:
                self._embeddings[intent] = self._model.encode(examples)

    def match(self, text: str) -> Tuple[str, float]:
        if self._model is None or not self._embeddings:
            return "conversation", 0.0

        try:
            import numpy as np
            text_embedding = self._model.encode([text])[0]

            best_intent = "conversation"
            best_similarity = 0.0

            for intent, embeddings in self._embeddings.items():
                similarities = np.dot(embeddings, text_embedding)
                max_sim = float(np.max(similarities))
                if max_sim > best_similarity:
                    best_similarity = max_sim
                    best_intent = intent

            return best_intent, best_similarity

        except Exception as e:
            self.log.error(f"Semantic matching failed: {e}")
            return "conversation", 0.0