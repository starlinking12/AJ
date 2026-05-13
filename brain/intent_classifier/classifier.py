"""
J.A.R.V.I.S. Intent Classifier
Main intent classification system. Routes user text to the correct intent.
Uses keyword matching, semantic matching, and embedding classification.
"""

from typing import Dict, Any, Optional

from brain.intent_classifier.keyword_matcher import KeywordMatcher
from brain.intent_classifier.semantic_matcher import SemanticMatcher
from brain.intent_classifier.embedding_classifier import EmbeddingClassifier
from brain.intent_classifier.few_shot_classifier import FewShotClassifier
from brain.intent_classifier.intent_labels import IntentLabels

from jarvis_core.logger import Logger


class IntentClassifier:
    """
    Multi-strategy intent classification.
    Falls back from fastest to most accurate:
    Keyword -> Semantic -> Embedding -> Few-Shot LLM
    """

    def __init__(self):
        self.log = Logger("IntentClassifier")
        self.keyword_matcher = KeywordMatcher()
        self.semantic_matcher = SemanticMatcher()
        self.embedding_classifier = EmbeddingClassifier()
        self.few_shot_classifier = FewShotClassifier()
        self.intent_labels = IntentLabels()
        self._initialized = False
        self._confidence_threshold = 0.6

    def initialize(self) -> bool:
        self.keyword_matcher.initialize()
        self.embedding_classifier.initialize()
        self._initialized = True
        self.log.info("Intent classifier ready.")
        return True

    def classify(self, text: str) -> str:
        if not text:
            return "unknown"

        text_lower = text.lower().strip()

        # Stage 1: Keyword matching (fastest)
        intent, confidence = self.keyword_matcher.match(text_lower)
        if confidence >= 0.9:
            self.log.debug(f"Keyword match: {intent} ({confidence:.2f})")
            return intent

        # Stage 2: Semantic matching
        intent, confidence = self.semantic_matcher.match(text_lower)
        if confidence >= self._confidence_threshold:
            self.log.debug(f"Semantic match: {intent} ({confidence:.2f})")
            return intent

        # Stage 3: Embedding classification
        intent, confidence = self.embedding_classifier.classify(text)
        if confidence >= self._confidence_threshold:
            self.log.debug(f"Embedding match: {intent} ({confidence:.2f})")
            return intent

        # Stage 4: Return best guess from keyword
        if confidence > 0.3:
            return intent

        return "conversation"

    def classify_with_confidence(self, text: str) -> Dict[str, Any]:
        intent = self.classify(text)
        return {
            "intent": intent,
            "label": self.intent_labels.get_label(intent),
            "requires_display": self.intent_labels.requires_display(intent),
            "requires_tool": self.intent_labels.requires_tool(intent),
        }

    def get_all_intents(self) -> list:
        return self.intent_labels.get_all_intents()