"""Integration tests for tool execution."""

import pytest


class TestToolIntegration:
    def test_search_to_cache_chain(self):
        from tools.search.search_cache import SearchCache
        from tools.search.content_summarizer import ContentSummarizer

        cache = SearchCache()
        cache.set("test query", {"results": [{"title": "Test", "content": "Content here."}]})

        cached = cache.get("test query")
        assert cached is not None

        summarizer = ContentSummarizer()
        summary = summarizer.summarize("Content here.", "test")
        assert len(summary) > 0

    def test_weather_to_voice_chain(self):
        from tools.weather.current_conditions import CurrentConditions
        from tools.weather.weather_cache import WeatherCache

        cache = WeatherCache(ttl=60)
        cc = CurrentConditions()

        weather_data = {
            "location": "London",
            "temperature": 15,
            "condition": "Cloudy",
            "units": "celsius",
        }
        cache.set("london", weather_data)
        cached = cache.get("london")
        assert cached is not None

        voice_text = cc.format_for_voice(cached)
        assert "London" in voice_text
        assert "Sir" in voice_text

    def test_map_cache_chain(self):
        from tools.maps.map_cache import MapCache

        cache = MapCache()
        cache.set("london", {"lat": 51.5, "lng": -0.1, "display_name": "London, UK"})

        result = cache.get("london")
        assert result is not None
        assert result["lat"] == 51.5