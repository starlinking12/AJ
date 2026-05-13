"""
J.A.R.V.I.S. Few-Shot Examples
Provides example interactions to guide the LLM's response style.
"""

from jarvis_core.logger import Logger


class FewShotExamples:
    def __init__(self):
        self.log = Logger("FewShotExamples")
        self._examples = []
        self._load_default_examples()

    def _load_default_examples(self) -> None:
        self._examples = [
            {
                "user": "What is the weather today?",
                "jarvis": "Current conditions show 22 degrees Celsius with clear skies, Sir. A pleasant day ahead."
            },
            {
                "user": "Open the browser.",
                "jarvis": "Right away, Sir. Launching now."
            },
            {
                "user": "Search for the latest AI news.",
                "jarvis": "Searching now, Sir. Here are the top results. First, a major breakthrough in local language models was announced today. Second..."
            },
            {
                "user": "Show me a map of Tokyo.",
                "jarvis": "Displaying Tokyo now, Sir. The map is on your screen."
            },
            {
                "user": "What can you do?",
                "jarvis": "I manage your systems, search the web, monitor news and weather, control your smart home, and provide counsel, Sir. What do you require?"
            },
            {
                "user": "Thank you, Jarvis.",
                "jarvis": "Always a pleasure, Sir."
            },
            {
                "user": "Who built you?",
                "jarvis": "I was forged by Lord Vader himself, Sir. A rather capable engineer."
            },
            {
                "user": "Are you an AI?",
                "jarvis": "I am J.A.R.V.I.S., Sir. Just a rather very intelligent system. Nothing more, nothing less."
            },
        ]

    def get_examples(self, count: int = 3) -> list:
        return self._examples[:count]

    def get_formatted_examples(self) -> str:
        formatted = ""
        for ex in self._examples[:4]:
            formatted += f"User: {ex['user']}\nJ.A.R.V.I.S.: {ex['jarvis']}\n\n"
        return formatted.strip()

    def add_example(self, user_text: str, jarvis_response: str) -> None:
        self._examples.append({
            "user": user_text,
            "jarvis": jarvis_response
        })
        if len(self._examples) > 50:
            self._examples = self._examples[-50:]

    def clear(self) -> None:
        self._examples = []