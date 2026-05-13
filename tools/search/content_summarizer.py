"""
J.A.R.V.I.S. Content Summarizer
Summarizes web content into concise summaries.
"""

from typing import Optional

from jarvis_core.logger import Logger


class ContentSummarizer:
    def __init__(self, max_sentences: int = 3):
        self.log = Logger("ContentSummarizer")
        self.max_sentences = max_sentences

    def summarize(self, content: str, query: str = "") -> str:
        if not content:
            return ""

        sentences = [s.strip() for s in content.replace("\n", " ").split(".") if len(s.strip()) > 20]

        if not sentences:
            return content[:300]

        if query:
            query_words = set(query.lower().split())
            scored = []
            for sentence in sentences:
                sentence_words = set(sentence.lower().split())
                score = len(query_words & sentence_words)
                scored.append((sentence, score))
            scored.sort(key=lambda x: x[1], reverse=True)
            top = [s[0] for s in scored[:self.max_sentences]]
            return ". ".join(top) + "."

        return ". ".join(sentences[:self.max_sentences]) + "."