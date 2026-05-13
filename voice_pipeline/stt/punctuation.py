"""
J.A.R.V.I.S. Punctuation Restorer
Adds punctuation and capitalization to raw transcription output.
"""

import re

from jarvis_core.logger import Logger


class PunctuationRestorer:
    def __init__(self):
        self.log = Logger("PunctuationRestorer")
        self._initialized = False
        self._model = None

    def initialize(self) -> bool:
        try:
            from deepmultilingualpunctuation import PunctuationModel
            self._model = PunctuationModel()
            self._initialized = True
            self.log.info("Punctuation model loaded.")
            return True
        except ImportError:
            self.log.warn("deepmultilingualpunctuation not installed. Using basic rules.")
            self._initialized = True
            return True
        except Exception as e:
            self.log.warn(f"Punctuation model failed: {e}. Using basic rules.")
            self._initialized = True
            return True

    def restore(self, text: str) -> str:
        if not text:
            return text

        if self._model is not None:
            try:
                return self._model.restore_punctuation(text)
            except Exception:
                pass

        return self._basic_restore(text)

    def _basic_restore(self, text: str) -> str:
        text = text.strip()
        if not text:
            return text

        text = text[0].upper() + text[1:] if len(text) > 1 else text.upper()

        if text[-1] not in ".!?":
            text += "."

        question_words = ["what", "how", "who", "where", "when", "why", "can", "could", "would", "will", "is", "are", "do", "does", "did", "should"]
        first_word = text.split()[0].lower() if text.split() else ""
        if first_word in question_words:
            if text.endswith("."):
                text = text[:-1] + "?"

        return text