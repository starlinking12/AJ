"""
J.A.R.V.I.S. Fallback Manager
Handles graceful degradation when components fail.
"""

from typing import Dict, Any, Optional

from jarvis_core.logger import Logger


class FallbackManager:
    def __init__(self):
        self.log = Logger("FallbackManager")
        self._fallbacks: Dict[str, str] = {
            "search_offline": "I am unable to search at the moment, Sir. My connection appears to be offline.",
            "llm_timeout": "My apologies, Sir. I seem to be thinking slowly. Could you repeat that?",
            "tool_error": "I encountered an issue executing that command, Sir. Would you like me to try again?",
            "memory_error": "I am having trouble accessing my memory banks, Sir. Proceeding with limited context.",
            "voice_error": "I can hear you, Sir, but I am having difficulty processing the audio.",
            "wake_word_error": "My listening systems encountered an error, Sir. Please try again.",
        }

    def get_fallback_response(self, error_type: str) -> str:
        return self._fallbacks.get(
            error_type,
            "I seem to be experiencing a technical difficulty, Sir. One moment please."
        )

    def handle_error(self, error_type: str, exception: Optional[Exception] = None) -> Dict[str, Any]:
        if exception:
            self.log.error(f"Fallback triggered: {error_type} - {exception}")
        else:
            self.log.warn(f"Fallback triggered: {error_type}")

        return {
            "text": self.get_fallback_response(error_type),
            "error_type": error_type,
            "is_fallback": True,
        }

    def register_fallback(self, error_type: str, response: str) -> None:
        self._fallbacks[error_type] = response