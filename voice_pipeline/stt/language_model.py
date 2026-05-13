"""
J.A.R.V.I.S. Language Model
Handles language model scoring and text correction.
"""

from typing import List, Optional

from jarvis_core.logger import Logger


class LanguageModel:
    def __init__(self):
        self.log = Logger("LanguageModel")
        self._initialized = False
        self._vocabulary = set()
        self._load_default_vocabulary()

    def _load_default_vocabulary(self) -> None:
        common_words = [
            "jarvis", "wake", "up", "sleep", "open", "close", "show",
            "map", "weather", "news", "camera", "music", "play", "stop",
            "search", "find", "what", "how", "who", "where", "when",
            "system", "status", "settings", "screen", "volume", "brightness",
            "london", "paris", "new york", "tokyo", "temperature",
            "sir", "please", "thanks", "thank you"
        ]
        self._vocabulary.update(common_words)

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info(f"Language model ready. Vocabulary: {len(self._vocabulary)} words")
        return True

    def score(self, text: str) -> float:
        words = text.lower().split()
        if not words:
            return 0.0
        matches = sum(1 for w in words if w in self._vocabulary)
        return matches / len(words)

    def correct(self, text: str) -> str:
        corrections = {
            "jarvi": "Jarvis",
            "jarva": "Jarvis",
            "jarves": "Jarvis",
        }
        words = text.split()
        corrected = [corrections.get(w.lower(), w) for w in words]
        return " ".join(corrected)

    def add_word(self, word: str) -> None:
        self._vocabulary.add(word.lower())