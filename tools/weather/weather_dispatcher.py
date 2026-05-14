"""
J.A.R.V.I.S. Weather Dispatcher
Routes weather requests to the best available weather service.
Primary: Open-Meteo (free, no API key, global coverage).
Secondary: NOAA (free, US-focused).
"""

from typing import Dict, Any, Optional

from tools.weather.openmeteo_client import OpenMeteoClient
from tools.weather.noaa_client import NOAAClient
from tools.weather.current_conditions import CurrentConditions
from tools.weather.forecast import Forecast
from tools.weather.alerts import WeatherAlerts
from tools.weather.air_quality import AirQuality
from tools.weather.weather_cache import WeatherCache

from jarvis_core.logger import Logger


class WeatherDispatcher:
    def __init__(self):
        self.log = Logger("WeatherDispatcher")
        self.cache = WeatherCache()
        self.current_conditions = CurrentConditions()
        self.forecast = Forecast()
        self.alerts = WeatherAlerts()
        self.air_quality = AirQuality()
        self._providers = []
        self._initialized = False

    def initialize(self) -> bool:
        self._providers = [
            OpenMeteoClient(),
            NOAAClient(),
        ]

        for provider in self._providers:
            try:
                if provider.initialize():
                    self.log.info(f"Weather provider ready: {provider.__class__.__name__}")
            except Exception as e:
                self.log.warn(f"Weather provider unavailable: {provider.__class__.__name__} - {e}")

        self._initialized = True
        self.log.info("Weather dispatcher ready.")
        return True

    def get_current(self, location: str, units: str = "celsius") -> Dict[str, Any]:
        cache_key = f"current_{location}_{units}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        for provider in self._providers:
            try:
                result = provider.get_current(location, units)
                if result and result.get("temperature") is not None:
                    self.cache.set(cache_key, result)
                    return result
            except Exception as e:
                self.log.warn(f"Provider {provider.__class__.__name__} failed: {e}")
                continue

        return {"error": "No weather providers available.", "location": location}

    def get_forecast(self, location: str, days: int = 7, units: str = "celsius") -> Dict[str, Any]:
        cache_key = f"forecast_{location}_{days}_{units}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        for provider in self._providers:
            try:
                result = provider.get_forecast(location, days, units)
                if result and result.get("daily"):
                    self.cache.set(cache_key, result)
                    return result
            except Exception as e:
                self.log.warn(f"Forecast failed for {provider.__class__.__name__}: {e}")
                continue

        return {"error": "No forecast available.", "location": location}

    def get_alerts(self, location: str) -> Dict[str, Any]:
        return self.alerts.get_alerts(location)

    def get_air_quality(self, location: str) -> Dict[str, Any]:
        return self.air_quality.get(location)

    def format_for_voice(self, weather_data: Dict[str, Any]) -> str:
        return self.current_conditions.format_for_voice(weather_data)