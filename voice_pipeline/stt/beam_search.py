"""
J.A.R.V.I.S. Beam Search
Implements beam search decoding for transcription candidates.
"""

from typing import List, Tuple

from jarvis_core.logger import Logger


class BeamSearch:
    def __init__(self, beam_width: int = 5):
        self.log = Logger("BeamSearch")
        self.beam_width = beam_width
        self._candidates: List[Tuple[str, float]] = []

    def search(self, candidates: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
        sorted_candidates = sorted(candidates, key=lambda x: x[1], reverse=True)
        self._candidates = sorted_candidates[:self.beam_width]
        return self._candidates

    def get_best(self) -> Tuple[str, float]:
        if not self._candidates:
            return ("", 0.0)
        return self._candidates[0]

    def get_all(self, min_score: float = 0.0) -> List[Tuple[str, float]]:
        return [(text, score) for text, score in self._candidates if score >= min_score]

    def reset(self) -> None:
        self._candidates = []