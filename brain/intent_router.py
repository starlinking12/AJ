"""
J.A.R.V.I.S. Intent Router
Routes classified intents to the appropriate handler or tool.
"""

from typing import Dict, Any, Optional

from jarvis_core.logger import Logger


class IntentRouter:
    """
    Maps intents to their corresponding handlers.
    Supports dynamic registration of new intent handlers.
    """

    def __init__(self):
        self.log = Logger("IntentRouter")
        self._handlers: Dict[str, callable] = {}
        self._register_default_handlers()

    def _register_default_handlers(self) -> None:
        self._handlers["search"] = self._handle_search
        self._handlers["news"] = self._handle_news
        self._handlers["weather"] = self._handle_weather
        self._handlers["map"] = self._handle_map
        self._handlers["system"] = self._handle_system
        self._handlers["camera"] = self._handle_camera
        self._handlers["music"] = self._handle_music
        self._handlers["conversation"] = self._handle_conversation
        self._handlers["unknown"] = self._handle_unknown

    def route(self, intent: str, params: Dict[str, Any]) -> Any:
        handler = self._handlers.get(intent)
        if handler is None:
            handler = self._handlers["conversation"]

        self.log.info(f"Routing intent '{intent}' to handler.")
        return handler(params)

    def register_handler(self, intent: str, handler: callable) -> None:
        self._handlers[intent] = handler
        self.log.info(f"Handler registered for intent: {intent}")

    def get_registered_intents(self) -> list:
        return list(self._handlers.keys())

    # Default handlers (stubs - actual logic in tools/)
    def _handle_search(self, params: Dict) -> Dict:
        return {"action": "search", "params": params}

    def _handle_news(self, params: Dict) -> Dict:
        return {"action": "news", "params": params}

    def _handle_weather(self, params: Dict) -> Dict:
        return {"action": "weather", "params": params}

    def _handle_map(self, params: Dict) -> Dict:
        return {"action": "map", "params": params}

    def _handle_system(self, params: Dict) -> Dict:
        return {"action": "system", "params": params}

    def _handle_camera(self, params: Dict) -> Dict:
        return {"action": "camera", "params": params}

    def _handle_music(self, params: Dict) -> Dict:
        return {"action": "music", "params": params}

    def _handle_conversation(self, params: Dict) -> Dict:
        return {"action": "respond", "params": params}

    def _handle_unknown(self, params: Dict) -> Dict:
        return {"action": "ask_clarification", "params": params}