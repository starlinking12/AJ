"""
J.A.R.V.I.S. Citation Formatter
Formats search results into natural language citations.
"""

from typing import List, Dict

from jarvis_core.logger import Logger


class CitationFormatter:
    def __init__(self):
        self.log = Logger("CitationFormatter")

    def format(self, results: List[Dict]) -> str:
        if not results:
            return ""

        citations = []
        for i, r in enumerate(results[:5], 1):
            title = r.get("title", "Unknown source")
            url = r.get("url", "")
            if title and url:
                citations.append(f"[{i}] {title} - {url}")
            elif title:
                citations.append(f"[{i}] {title}")

        return "\n".join(citations)

    def format_inline(self, results: List[Dict]) -> str:
        if not results:
            return ""

        sources = []
        for r in results[:3]:
            title = r.get("title", "")
            if title:
                sources.append(title)

        if sources:
            return "According to " + ", ".join(sources) + "."
        return ""