"""
J.A.R.V.I.S. Hotword Boosting
Boosts recognition probability for specific words and phrases.
Ensures important commands are never misheard.
"""

from typing import List, Tuple

from jarvis_core.logger import Logger


class HotwordBooster:
    def __init__(self):
        self.log = Logger("HotwordBooster")
        self._hotwords: List[Tuple[str, float]] = []
        self._load_default_hotwords()

    def _load_default_hotwords(self) -> None:
        defaults = [
            ("jarvis", 2.0),
            ("wake up", 2.0),
            ("sleep", 2.0),
            ("open", 3.0),
            ("close", 3.0),
            ("map", 3.0),
            ("weather", 3.0),
            ("news", 3.0),
            ("camera", 3.0),
            ("music", 3.0),
            ("system", 2.0),
            ("screen", 2.0),
            ("stop", 3.0),
            ("shutdown", 5.0),
        ]
        self._hotwords = defaults

    def get_boost_list(self) -> List[Tuple[str, float]]:
        return self._hotwords

    def add_hotword(self, word: str, boost: float = 2.0) -> None:
        self._hotwords.append((word.lower(), boost))
        self.log.info(f"Hotword added: {word} (boost: {boost})")

    def remove_hotword(self, word: str) -> None:
        self._hotwords = [
            (w, b) for w, b in self._hotwords if w != word.lower()
        ]

    def get_boost_for(self, word: str) -> float:
        for w, b in self._hotwords:
            if w == word.lower():
                return b
        return 1.0