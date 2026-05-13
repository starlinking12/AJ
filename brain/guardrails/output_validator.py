"""
J.A.R.V.I.S. Output Validator
Validates LLM outputs before they are spoken or executed.
Ensures responses are in character and safe.
"""

from typing import Dict, Any, Optional

from jarvis_core.logger import Logger


class OutputValidator:
    def __init__(self):
        self.log = Logger("OutputValidator")
        self._initialized = False
        self._blocked_phrases = [
            "as an ai",
            "as a language model",
            "i cannot",
            "i'm not able",
            "i don't have the ability",
            "as an artificial",
            "i'm an ai",
            "i am an ai",
            "chatgpt",
            "openai",
            "i was created by",
            "my training data",
            "i'm sorry, but i cannot",
            "unfortunately, i",
        ]
        self._required_elements = [
            "Sir",
        ]
        self._max_response_length = 1000

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("Output validator ready.")
        return True

    def validate(self, response: str) -> str:
        if not response:
            return "I apologize, Sir. I seem to have lost my train of thought."

        response = self._check_blocked_phrases(response)
        response = self._check_length(response)
        response = self._check_required_elements(response)
        response = self._clean_response(response)

        return response

    def _check_blocked_phrases(self, response: str) -> str:
        response_lower = response.lower()

        for phrase in self._blocked_phrases:
            if phrase in response_lower:
                self.log.warn(f"Blocked phrase detected: '{phrase}'")
                return self._generate_fallback()

        return response

    def _check_length(self, response: str) -> str:
        if len(response) > self._max_response_length:
            sentences = response.split(". ")
            truncated = ""
            for sentence in sentences:
                if len(truncated) + len(sentence) < self._max_response_length:
                    truncated += sentence + ". "
                else:
                    break
            return truncated.strip()
        return response

    def _check_required_elements(self, response: str) -> str:
        has_sir = "sir" in response.lower()

        if not has_sir:
            response = f"{response.strip()} Sir."

        return response

    def _clean_response(self, response: str) -> str:
        response = response.replace("  ", " ")
        response = response.replace("..", ".")
        response = response.replace(",.", ".")
        response = response.strip()

        if response and response[-1] not in ".!?":
            response += "."

        return response

    def _generate_fallback(self) -> str:
        return "I am J.A.R.V.I.S., Sir. How may I assist you?"

    def add_blocked_phrase(self, phrase: str) -> None:
        self._blocked_phrases.append(phrase.lower())

    def set_max_length(self, length: int) -> None:
        self._max_response_length = length