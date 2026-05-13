"""
J.A.R.V.I.S. Keyword Matcher
Fast keyword-based intent detection.
"""

from typing import Dict, List, Tuple

from jarvis_core.logger import Logger


class KeywordMatcher:
    def __init__(self):
        self.log = Logger("KeywordMatcher")
        self._patterns: Dict[str, List[str]] = {}
        self._initialized = False

    def initialize(self) -> bool:
        self._load_patterns()
        self._initialized = True
        return True

    def _load_patterns(self) -> None:
        self._patterns = {
            "search": [
                "search for", "look up", "find", "google", "what is", "who is",
                "tell me about", "information on", "research", "define", "explain",
                "how does", "why is", "where can i find",
            ],
            "news": [
                "news", "headlines", "what's happening", "current events",
                "latest", "breaking", "today's news", "news update",
                "what is in the news", "tell me the news",
            ],
            "weather": [
                "weather", "temperature", "forecast", "how hot", "how cold",
                "will it rain", "is it sunny", "humidity", "wind",
                "what's the weather", "weather today", "weather tomorrow",
            ],
            "map": [
                "show map", "map of", "where is", "navigate to", "directions to",
                "location of", "show me", "find on map", "route to",
            ],
            "system": [
                "open", "close app", "launch", "start program", "volume up",
                "volume down", "mute", "brightness", "shutdown computer",
                "restart", "lock screen", "sleep computer",
            ],
            "camera": [
                "camera", "webcam", "take a picture", "take a photo",
                "what do you see", "open camera", "close camera",
                "show camera", "hide camera",
            ],
            "music": [
                "play music", "play song", "spotify", "playlist", "pause music",
                "resume music", "skip song", "next track", "previous track",
                "what's playing", "stop music",
            ],
        }

    def match(self, text: str) -> Tuple[str, float]:
        best_intent = "conversation"
        best_score = 0.0

        for intent, patterns in self._patterns.items():
            for pattern in patterns:
                if pattern in text:
                    score = len(pattern) / len(text.split())
                    if score > best_score:
                        best_score = score
                        best_intent = intent

        if text.startswith("open ") and len(text) > 5:
            if best_intent == "conversation":
                best_intent = "system"
                best_score = 0.7

        if text.startswith("play ") and len(text) > 5:
            if best_intent == "conversation":
                best_intent = "music"
                best_score = 0.7

        if text.startswith("show me ") or text.startswith("show map"):
            if best_intent == "conversation":
                best_intent = "map"
                best_score = 0.8

        confidence = min(best_score, 1.0)
        return best_intent, confidence

    def add_pattern(self, intent: str, pattern: str) -> None:
        if intent not in self._patterns:
            self._patterns[intent] = []
        self._patterns[intent].append(pattern.lower())