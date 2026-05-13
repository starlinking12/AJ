"""
J.A.R.V.I.S. Deep Search
Multi-pass deep search that scrapes and synthesizes results.
"""

from typing import Dict, Any, List

from tools.search.scraper import Scraper
from tools.search.content_summarizer import ContentSummarizer
from tools.search.citation_formatter import CitationFormatter

from jarvis_core.logger import Logger


class DeepSearcher:
    def __init__(self, dispatcher):
        self.log = Logger("DeepSearcher")
        self.dispatcher = dispatcher
        self.scraper = Scraper()
        self.summarizer = ContentSummarizer()
        self.citation = CitationFormatter()

    def search(self, query: str, max_sources: int = 5) -> Dict[str, Any]:
        initial_results = self.dispatcher.search(query, depth="quick", max_results=max_sources)

        if not initial_results.get("results"):
            return initial_results

        enriched = []
        for result in initial_results["results"]:
            url = result.get("url")
            if url:
                try:
                    page_content = self.scraper.scrape(url)
                    summary = self.summarizer.summarize(page_content, query)
                    result["full_content"] = page_content[:2000]
                    result["summary"] = summary
                except Exception as e:
                    self.log.warn(f"Scraping failed for {url}: {e}")
                    result["summary"] = result.get("content", "")
            enriched.append(result)

        synthesis = self._synthesize(query, enriched)
        citations = self.citation.format(enriched)

        return {
            "query": query,
            "results": enriched,
            "synthesis": synthesis,
            "citations": citations,
            "source": "deep_search",
        }

    def _synthesize(self, query: str, results: List[Dict]) -> str:
        if not results:
            return "No results found."

        key_points = []
        for i, r in enumerate(results[:3]):
            summary = r.get("summary", r.get("content", ""))
            if summary:
                key_points.append(f"From {r.get('title', 'source')}: {summary[:200]}")

        return " ".join(key_points) if key_points else "Results collected but could not synthesize."