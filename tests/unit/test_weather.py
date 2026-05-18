"""Tests for weather tools."""

import pytest
from tools.weather.current_conditions import CurrentConditions
from tools.weather.forecast import Forecast
from tools.weather.weather_cache import WeatherCache


class TestCurrentConditions:
    def test_format_basic(self):
        cc = CurrentConditions()
        data = {
            "location": "London",
            "temperature": 18,
            "condition": "Partly cloudy",
            "humidity": 65,
            "wind_speed": 12,
            "units": "celsius",
        }
        result = cc.format_for_voice(data)
        assert "London" in result
        assert "18" in result
        assert "Sir" in result

    def test_format_error(self):
        cc = CurrentConditions()
        result = cc.format_for_voice({"error": "City not found"})
        assert "unable" in result.lower()

    def test_icon_suggestion(self):
        cc = CurrentConditions()
        assert cc.get_icon_suggestion(0) == "sunny"
        assert cc.get_icon_suggestion(61) == "rain"
        assert cc.get_icon_suggestion(95) == "thunderstorm"


class TestForecast:
    def test_format_basic(self):
        f = Forecast()
        data = {
            "location": "Paris",
            "daily": [
                {"date": "2026-01-01", "temp_max": 10, "temp_min": 2, "condition": "Clear"},
                {"date": "2026-01-02", "temp_max": 12, "temp_min": 4, "condition": "Cloudy"},
            ],
            "units": "celsius",
        }
        result = f.format_for_voice(data, days=2)
        assert "Paris" in result
        assert "Sir" in result

    def test_format_empty(self):
        f = Forecast()
        result = f.format_for_voice({"error": "No data"})
        assert "unavailable" in result.lower()


class TestWeatherCache:
    def test_cache_works(self):
        cache = WeatherCache(ttl=60)
        cache.set("london", {"temp": 15})
        assert cache.get("london")["temp"] == 15

    def test_expiry(self):
        cache = WeatherCache(ttl=0)
        cache.set("london", {"temp": 15})
        import time
        time.sleep(0.1)
        assert cache.get("london") is None