"""
J.A.R.V.I.S. Intent Labels
Defines all possible intents and their properties.
"""

from typing import Dict, List


class IntentLabels:
    def __init__(self):
        self._intents: Dict[str, Dict] = {}
        self._load_intents()

    def _load_intents(self) -> None:
        self._intents = {
            "search": {
                "label": "Web Search",
                "description": "Search the web for information",
                "requires_display": True,
                "requires_tool": True,
                "tool": "web_search",
                "examples": [
                    "search for",
                    "look up",
                    "find information about",
                    "google",
                    "what is",
                    "who is",
                    "tell me about",
                ],
            },
            "news": {
                "label": "News",
                "description": "Fetch current news headlines",
                "requires_display": True,
                "requires_tool": True,
                "tool": "get_news",
                "examples": [
                    "news",
                    "headlines",
                    "what's happening",
                    "current events",
                    "latest news",
                    "breaking news",
                ],
            },
            "weather": {
                "label": "Weather",
                "description": "Get weather conditions and forecast",
                "requires_display": True,
                "requires_tool": True,
                "tool": "get_weather",
                "examples": [
                    "weather",
                    "temperature",
                    "forecast",
                    "how hot",
                    "how cold",
                    "will it rain",
                    "is it sunny",
                ],
            },
            "map": {
                "label": "Map",
                "description": "Display maps and locations",
                "requires_display": True,
                "requires_tool": True,
                "tool": "show_map",
                "examples": [
                    "show map",
                    "map of",
                    "where is",
                    "navigate to",
                    "directions to",
                    "location of",
                ],
            },
            "system": {
                "label": "System Control",
                "description": "Control the computer",
                "requires_display": False,
                "requires_tool": True,
                "tool": "system_command",
                "examples": [
                    "open",
                    "close",
                    "launch",
                    "start",
                    "stop",
                    "volume",
                    "brightness",
                    "shutdown",
                    "restart",
                    "sleep computer",
                ],
            },
            "camera": {
                "label": "Camera",
                "description": "Control the camera",
                "requires_display": True,
                "requires_tool": True,
                "tool": "open_camera",
                "examples": [
                    "camera",
                    "webcam",
                    "take a picture",
                    "show me",
                    "what do you see",
                    "open camera",
                    "close camera",
                ],
            },
            "music": {
                "label": "Music",
                "description": "Play music",
                "requires_display": False,
                "requires_tool": True,
                "tool": "play_music",
                "examples": [
                    "play",
                    "music",
                    "song",
                    "spotify",
                    "playlist",
                    "pause",
                    "resume",
                    "skip",
                ],
            },
            "conversation": {
                "label": "Conversation",
                "description": "General conversation",
                "requires_display": False,
                "requires_tool": False,
                "tool": None,
                "examples": [
                    "hello",
                    "hi",
                    "how are you",
                    "thank you",
                    "good morning",
                    "good night",
                    "who are you",
                    "what can you do",
                ],
            },
            "unknown": {
                "label": "Unknown",
                "description": "Unable to classify intent",
                "requires_display": False,
                "requires_tool": False,
                "tool": None,
                "examples": [],
            },
        }

    def get_label(self, intent: str) -> str:
        return self._intents.get(intent, {}).get("label", "Unknown")

    def requires_display(self, intent: str) -> bool:
        return self._intents.get(intent, {}).get("requires_display", False)

    def requires_tool(self, intent: str) -> bool:
        return self._intents.get(intent, {}).get("requires_tool", False)

    def get_tool(self, intent: str) -> str:
        return self._intents.get(intent, {}).get("tool")

    def get_examples(self, intent: str) -> List[str]:
        return self._intents.get(intent, {}).get("examples", [])

    def get_all_intents(self) -> List[str]:
        return list(self._intents.keys())