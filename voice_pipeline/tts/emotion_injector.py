"""
J.A.R.V.I.S. Emotion Injector
Adds emotional markers and SSML tags to text before synthesis.
Helps Jarvis sound more natural and expressive.
"""

from typing import Dict

from jarvis_core.logger import Logger


class EmotionInjector:
    def __init__(self):
        self.log = Logger("EmotionInjector")
        self._emotion_map: Dict[str, str] = {
            "happy": "enthusiastic",
            "sad": "subdued",
            "urgent": "fast",
            "calm": "slow",
            "formal": "precise",
        }

    def process(self, text: str, emotion: str = "formal") -> str:
        text = self._add_ssml_breaks(text)
        text = self._normalize_text(text)
        return text

    def _add_ssml_breaks(self, text: str) -> str:
        if text.startswith("<speak>"):
            return text

        parts = text.split(". ")
        if len(parts) > 1:
            text = " <break time='200ms'/> ".join(parts)

        parts = text.split(", ")
        text = " <break time='100ms'/> ".join(parts)

        return text

    def _normalize_text(self, text: str) -> str:
        text = text.replace("Sir.", "Sir")
        text = text.replace("Mr.", "Mister")
        text = text.replace("Dr.", "Doctor")

        return text

    def set_emotion(self, emotion: str) -> str:
        return self._emotion_map.get(emotion, "formal")

    def get_available_emotions(self) -> list:
        return list(self._emotion_map.keys())