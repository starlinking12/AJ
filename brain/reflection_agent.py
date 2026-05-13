"""
J.A.R.V.I.S. Reflection Agent
Self-corrects and refines LLM outputs before speaking.
Uses LLM-as-judge pattern for quality assurance.
"""

from typing import Optional

from jarvis_core.logger import Logger


class ReflectionAgent:
    def __init__(self, llm_client):
        self.log = Logger("ReflectionAgent")
        self.llm = llm_client
        self._enabled = True
        self._threshold = 0.7

    def should_reflect(self, response: str) -> bool:
        if not self._enabled:
            return False

        if len(response) < 10:
            return True

        problem_phrases = [
            "as an ai", "as a language model", "i cannot", "i'm not able",
            "i don't have", "i'm sorry, but", "unfortunately i",
            "i am an ai", "i'm an ai", "as an artificial",
        ]
        for phrase in problem_phrases:
            if phrase in response.lower():
                return True

        return False

    def refine(self, original_response: str, user_query: str) -> str:
        self.log.info("Refining response...")

        reflection_prompt = f"""You are J.A.R.V.I.S., a sophisticated AI assistant.
Your previous response was: "{original_response}"

It contained phrases that an advanced AI butler would never say.
Rewrite the response to be professional, helpful, and in character.
Never mention being an AI, language model, or use phrases like "I cannot" or "As an AI".
Always address the user as "Sir".

Original query: {user_query}

Refined response:"""

        try:
            refined = self.llm.generate(
                system_prompt="You are J.A.R.V.I.S. Be concise and professional.",
                user_message=reflection_prompt,
                context=""
            )
            return refined if refined else original_response
        except Exception as e:
            self.log.error(f"Reflection failed: {e}")
            return original_response

    def enable(self) -> None:
        self._enabled = True

    def disable(self) -> None:
        self._enabled = False