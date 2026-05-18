"""Tests for web search tools."""

import pytest
from tools.search.search_cache import SearchCache
from tools.search.content_summarizer import ContentSummarizer
from tools.search.citation_formatter import CitationFormatter


class TestSearchCache:
    def test_get_set(self):
        cache = SearchCache(ttl=60)
        cache.set("query", {"results": ["test"]})
        result = cache.get("query")
        assert result is not None
        assert result["results"] == ["test"]

    def test_miss(self):
        cache = SearchCache()
        result = cache.get("nonexistent")
        assert result is None

    def test_clear(self):
        cache = SearchCache()
        cache.set("q", {"data": 1})
        cache.clear()
        assert cache.get("q") is None


class TestContentSummarizer:
    def test_summarize_basic(self):
        cs = ContentSummarizer(max_sentences=2)
        text = "This is sentence one. This is sentence two. This is sentence three."
        result = cs.summarize(text)
        sentences = result.split(". ")
        assert len(sentences) <= 2

    def test_summarize_empty(self):
        cs = ContentSummarizer()
        result = cs.summarize("")
        assert result == ""

    def test_summarize_with_query(self):
        cs = ContentSummarizer()
        text = "Python is a language. Weather is nice today. Python coding is fun."
        result = cs.summarize(text, query="Python")
        assert "Python" in result


class TestCitationFormatter:
    def test_format_citations(self):
        cf = CitationFormatter()
        results = [
            {"title": "Test Article", "url": "https://example.com"},
            {"title": "Another Source", "url": "https://test.com"},
        ]
        formatted = cf.format(results)
        assert "[1]" in formatted
        assert "Test Article" in formatted

    def test_format_empty(self):
        cf = CitationFormatter()
        assert cf.format([]) == ""

    def test_format_inline(self):
        cf = CitationFormatter()
        results = [{"title": "BBC News"}, {"title": "CNN"}]
        inline = cf.format_inline(results)
        assert "According to" in inline