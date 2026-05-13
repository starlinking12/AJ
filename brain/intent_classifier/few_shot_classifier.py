"""
J.A.R.V.I.S. Few-Shot Classifier
Uses the LLM itself for intent classification when other methods fail.
"""

from typing import Tuple, Optional

from jarvis_core.logger import Logger


class FewShotClassifier:
    def __init__(self):
        self.log = Logger("FewShotClassifier")
        self._llm_client = None
        self._initialized = False

    def initialize(self, llm_client=None) -> bool:
        self._llm_client = llm_client
        self._initialized = True
        return True

    def classify(self, text: str) -> Tuple[str, float]:
        if self._llm_client is None:
            return "conversation", 0.0

        try:
            prompt = f"""Classify the following user input into exactly one intent.
Valid intents: search, news, weather, map, system, camera, music, conversation.

Examples:
"what is the weather in London" -> weather
"open Chrome" -> system
"play some jazz" -> music
"show me a map of Paris" -> map
"what's the latest news" -> news
"who built the pyramids" -> search
"hello Jarvis" -> conversation

User input: "{text}"
Intent:"""

            result = self._llm_client.generate(
                system_prompt="Classify user intent. Respond with only the intent name.",
                user_message=prompt,
                context=""
            )

            result = result.strip().lower()

            valid_intents = ["search", "news", "weather", "map", "system", "camera", "music", "conversation"]
            for intent in valid_intents:
                if intent in result:
                    return intent, 0.8

            return "conversation", 0.5

        except Exception as e:
            self.log.error(f"Few-shot classification failed: {e}")
            return "conversation", 0.0