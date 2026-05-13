"""
J.A.R.V.I.S. Env Loader
Loads configuration from environment variables.
"""

import os
from typing import Any, Dict


class EnvLoader:
    @staticmethod
    def load() -> Dict[str, Any]:
        data = {}

        env_mappings = {
            "JARVIS_NAME": "jarvis_name",
            "JARVIS_WAKE_WORD": "wake_word",
            "JARVIS_SLEEP_WORD": "sleep_word",
            "JARVIS_USER_TITLE": "user_title",
            "OLLAMA_HOST": "ollama_host",
            "OLLAMA_MODEL": "ollama_model",
            "TTS_ENGINE": "tts_engine",
            "TTS_VOICE": "tts_voice",
            "STT_MODEL": "stt_model",
            "LOG_LEVEL": "log_level",
            "ENABLE_VISION": "enable_vision",
            "ENABLE_WEB_DASHBOARD": "enable_web_dashboard",
        }

        for env_key, config_key in env_mappings.items():
            value = os.environ.get(env_key)
            if value is not None:
                if value.lower() in ("true", "false"):
                    value = value.lower() == "true"
                data[config_key] = value

        api_keys = {}
        api_env_mappings = {
            "MISTRAL_API_KEY": "mistral",
            "GROQ_API_KEY": "groq",
            "TAVILY_API_KEY": "tavily",
            "TINYFISH_API_KEY": "tinyfish",
            "NEWSDATA_API_KEY": "newsdata",
            "MAPBOX_API_KEY": "mapbox",
        }
        for env_key, key_name in api_env_mappings.items():
            value = os.environ.get(env_key)
            if value:
                api_keys[key_name] = value

        if api_keys:
            data["api_keys"] = api_keys

        return data