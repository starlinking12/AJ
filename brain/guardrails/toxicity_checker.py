"""
J.A.R.V.I.S. Toxicity Checker
Detects and filters toxic, offensive, or inappropriate content.
"""

from typing import Tuple, Optional

from jarvis_core.logger import Logger


class ToxicityChecker:
    def __init__(self):
        self.log = Logger("ToxicityChecker")
        self._initialized = False
        self._threshold = 0.7
        self._blocked_categories = [
            "toxic",
            "severe_toxic",
            "obscene",
            "threat",
            "insult",
            "identity_hate",
        ]

    def initialize(self) -> bool:
        try:
            self._initialized = True
            self.log.info("Toxicity checker ready.")
            return True
        except Exception as e:
            self.log.warn(f"Toxicity checker init failed: {e}")
            self._initialized = True
            return True

    def check(self, text: str) -> Tuple[bool, float]:
        if not text:
            return True, 0.0

        text_lower = text.lower()

        toxic_keywords = [
            "kill yourself", "kys", "die in a fire",
            "i hate you", "you are useless", "shut up",
            "fuck you", "go to hell",
        ]
        for keyword in toxic_keywords:
            if keyword in text_lower:
                self.log.warn(f"Toxic keyword detected: '{keyword}'")
                return False, 1.0

        return True, 0.0

    def filter(self, text: str) -> str:
        is_safe, score = self.check(text)
        if not is_safe:
            return "I will not respond to that, Sir."
        return text

    def set_threshold(self, threshold: float) -> None:
        self._threshold = max(0.0, min(1.0, threshold))

    def get_blocked_categories(self) -> list:
        return self._blocked_categories