"""
J.A.R.V.I.S. Config Schema
Validates configuration data structure and types.
"""

from typing import Any, Dict


class ConfigSchema:
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def validate(self) -> Dict[str, Any]:
        validated = {}

        validated["jarvis_name"] = self.data.get("jarvis_name", "J.A.R.V.I.S.")
        validated["wake_word"] = self.data.get("wake_word", "wake up")
        validated["sleep_word"] = self.data.get("sleep_word", "sleep")
        validated["user_title"] = self.data.get("user_title", "Sir")

        validated["ollama_host"] = self.data.get("ollama_host", "http://localhost:11434")
        validated["ollama_model"] = self.data.get("ollama_model", "llama3.2:3b")

        validated["tts_engine"] = self.data.get("tts_engine", "piper")
        validated["tts_voice"] = self.data.get("tts_voice", "jarvis_british_male")
        validated["stt_model"] = self.data.get("stt_model", "base")

        validated["log_level"] = self.data.get("log_level", "INFO")
        validated["max_restarts"] = self.data.get("max_restarts", 3)

        validated["enable_vision"] = self.data.get("enable_vision", False)
        validated["enable_web_dashboard"] = self.data.get("enable_web_dashboard", False)

        validated["api_keys"] = self.data.get("api_keys", {})

        return validated