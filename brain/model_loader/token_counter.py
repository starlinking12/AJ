"""
J.A.R.V.I.S. Token Counter
Accurate token counting for LLM context management.
"""

from typing import Optional

from jarvis_core.logger import Logger


class TokenCounter:
    def __init__(self):
        self.log = Logger("TokenCounter")
        self._tokenizer = None
        self._initialized = False

    def initialize(self, model_name: str = "llama3.2") -> bool:
        try:
            import tiktoken

            tokenizer_map = {
                "llama3.2": "cl100k_base",
                "llama3": "cl100k_base",
                "mistral": "cl100k_base",
                "phi3": "cl100k_base",
            }

            encoding_name = tokenizer_map.get(model_name, "cl100k_base")
            self._tokenizer = tiktoken.get_encoding(encoding_name)
            self._initialized = True
            self.log.info(f"Token counter ready. Encoding: {encoding_name}")
            return True

        except ImportError:
            self.log.warn("tiktoken not installed. Using estimate mode.")
            self._initialized = True
            return True
        except Exception as e:
            self.log.warn(f"Token counter init failed: {e}")
            self._initialized = True
            return True

    def count(self, text: str) -> int:
        if self._tokenizer:
            try:
                return len(self._tokenizer.encode(text))
            except Exception:
                pass
        return len(text) // 4

    def count_messages(self, messages: list) -> int:
        total = 0
        for msg in messages:
            total += self.count(msg.get("content", ""))
        return total

    def truncate_to_limit(self, text: str, max_tokens: int) -> str:
        if self.count(text) <= max_tokens:
            return text

        words = text.split()
        truncated = []
        current_tokens = 0

        for word in words:
            word_tokens = self.count(word)
            if current_tokens + word_tokens > max_tokens:
                break
            truncated.append(word)
            current_tokens += word_tokens

        return " ".join(truncated) + "..."