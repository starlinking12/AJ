"""
J.A.R.V.I.S. Multi-Pass Search
Executes multiple search passes with refined queries for comprehensive results.
"""

from typing import Dict, Any, List

from jarvis_core.logger import Logger


class MultiPassSearch:
    def __init__(self, dispatcher):
        self.log = Logger("MultiPassSearch")
        self.dispatcher = dispatcher

    def search(self, query: str, passes: int = 3) -> Dict[str, Any]:
        all_results = []
        seen_urls = set()

        queries = [query]
        queries.extend(self._generate_related_queries(query, passes - 1))

        for q in queries:
            result = self.dispatcher.search(q, max_results=5)
            for r in result.get("results", []):
                url = r.get("url")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    all_results.append(r)

        return {
            "query": query,
            "results": all_results,
            "total_sources": len(all_results),
            "search_passes": passes,
        }

    def _generate_related_queries(self, query: str, count: int) -> List[str]:
        related = []
        prefixes = ["latest", "best", "how to", "what is", "guide to"]
        for prefix in prefixes[:count]:
            if prefix not in query.lower():
                related.append(f"{prefix} {query}")
        return related