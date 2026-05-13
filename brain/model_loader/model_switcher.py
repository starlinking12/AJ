"""
J.A.R.V.I.S. Model Switcher
Dynamically switches between LLM models based on task requirements.
"""

from typing import Optional

from jarvis_core.logger import Logger


class ModelSwitcher:
    def __init__(self, ollama_client):
        self.log = Logger("ModelSwitcher")
        self.client = ollama_client
        self._current_model: Optional[str] = None
        self._task_model_map = {
            "search": "llama3.2:3b",
            "news": "llama3.2:3b",
            "weather": "llama3.2:3b",
            "map": "llama3.2:3b",
            "system": "llama3.2:3b",
            "conversation": "llama3.2:8b",
            "code": "llama3.2:8b",
            "complex": "llama3.2:8b",
            "default": "llama3.2:3b",
        }

    def switch_for_task(self, intent: str) -> str:
        model = self._task_model_map.get(intent, self._task_model_map["default"])
        self.log.info(f"Model for intent '{intent}': {model}")
        self._current_model = model
        return model

    def set_model(self, model_name: str) -> bool:
        available = self.client.list_models()
        if model_name in available:
            self._current_model = model_name
            self.log.info(f"Model set to: {model_name}")
            return True
        self.log.warn(f"Model not available: {model_name}")
        return False

    def get_current_model(self) -> Optional[str]:
        return self._current_model

    def add_task_mapping(self, intent: str, model: str) -> None:
        self._task_model_map[intent] = model