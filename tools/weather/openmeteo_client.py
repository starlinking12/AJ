"""
J.A.R.V.I.S. Open-Meteo Client
Uses Open-Meteo API for global weather data.
Completely free. No API key required. No authentication.
Features: current conditions, 16-day forecast, historical data since 1940.
"""

import time
from typing import Dict, Any, Optional

import requests

from jarvis_core.logger import Logger


class OpenMeteoClient:
    def __init__(self):
        self.log = Logger("OpenMeteoClient")
        self.base_url = "https://api.open-meteo.com/v1"
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        self._initialized = False
        self._rate_limit_last = 0
        self._rate_limit_interval = 0.1

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("Open-Meteo client ready (free, no API key).")
        return True

    def _geocode(self, location: str) -> Optional[Dict[str, float]]:
        cached_coords = self._get_cached_coords(location)
        if cached_coords:
            return cached_coords

        self._rate_limit()
        try:
            params = {"name": location, "count": 1, "language": "en"}
            response = requests.get(self.geocoding_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                if results:
                    coords = {
                        "lat": results[0]["latitude"],
                        "lng": results[0]["longitude"],
                        "name": results[0].get("name", location),
                        "country": results[0].get("country", ""),
                        "timezone": results[0].get("timezone", "UTC"),
                    }
                    self._cache_coords(location, coords)
                    return coords
            return None

        except Exception as e:
            self.log.error(f"Open-Meteo geocoding failed: {e}")
            return None

    def get_current(self, location: str, units: str = "celsius") -> Dict[str, Any]:
        coords = self._geocode(location)
        if not coords:
            return {"error": f"Location not found: {location}"}

        self._rate_limit()
        try:
            temp_unit = "celsius" if units == "celsius" else "fahrenheit"

            params = {
                "latitude": coords["lat"],
                "longitude": coords["lng"],
                "current": [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "apparent_temperature",
                    "weather_code",
                    "wind_speed_10m",
                    "wind_direction_10m",
                    "precipitation",
                    "cloud_cover",
                    "pressure_msl",
                ],
                "temperature_unit": temp_unit,
                "timezone": coords.get("timezone", "UTC"),
            }

            response = requests.get(f"{self.base_url}/forecast", params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                current = data.get("current", {})

                return {
                    "location": coords["name"],
                    "country": coords.get("country", ""),
                    "temperature": current.get("temperature_2m"),
                    "feels_like": current.get("apparent_temperature"),
                    "humidity": current.get("relative_humidity_2m"),
                    "wind_speed": current.get("wind_speed_10m"),
                    "wind_direction": current.get("wind_direction_10m"),
                    "precipitation": current.get("precipitation"),
                    "cloud_cover": current.get("cloud_cover"),
                    "pressure": current.get("pressure_msl"),
                    "weather_code": current.get("weather_code"),
                    "condition": self._weather_code_to_text(current.get("weather_code", 0)),
                    "units": units,
                    "source": "open-meteo",
                }

            return {"error": f"API error: {response.status_code}"}

        except Exception as e:
            self.log.error(f"Open-Meteo current weather failed: {e}")
            return {"error": str(e)}

    def get_forecast(self, location: str, days: int = 7, units: str = "celsius") -> Dict[str, Any]:
        coords = self._geocode(location)
        if not coords:
            return {"error": f"Location not found: {location}"}

        self._rate_limit()
        try:
            temp_unit = "celsius" if units == "celsius" else "fahrenheit"

            params = {
                "latitude": coords["lat"],
                "longitude": coords["lng"],
                "daily": [
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "weather_code",
                    "precipitation_sum",
                    "wind_speed_10m_max",
                    "sunrise",
                    "sunset",
                ],
                "temperature_unit": temp_unit,
                "forecast_days": min(days, 16),
                "timezone": coords.get("timezone", "UTC"),
            }

            response = requests.get(f"{self.base_url}/forecast", params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                daily = data.get("daily", {})

                forecast_days = []
                for i in range(len(daily.get("time", []))):
                    forecast_days.append({
                        "date": daily["time"][i],
                        "temp_max": daily["temperature_2m_max"][i],
                        "temp_min": daily["temperature_2m_min"][i],
                        "condition": self._weather_code_to_text(daily["weather_code"][i]),
                        "precipitation": daily.get("precipitation_sum", [0])[i] if i < len(daily.get("precipitation_sum", [])) else 0,
                        "wind_max": daily.get("wind_speed_10m_max", [0])[i] if i < len(daily.get("wind_speed_10m_max", [])) else 0,
                        "sunrise": daily.get("sunrise", [""])[i] if i < len(daily.get("sunrise", [])) else "",
                        "sunset": daily.get("sunset", [""])[i] if i < len(daily.get("sunset", [])) else "",
                    })

                return {
                    "location": coords["name"],
                    "country": coords.get("country", ""),
                    "daily": forecast_days,
                    "units": units,
                    "source": "open-meteo",
                }

            return {"error": f"API error: {response.status_code}"}

        except Exception as e:
            self.log.error(f"Open-Meteo forecast failed: {e}")
            return {"error": str(e)}

    def _weather_code_to_text(self, code: int) -> str:
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail",
        }
        return weather_codes.get(code, "Unknown")

    def _rate_limit(self) -> None:
        elapsed = time.time() - self._rate_limit_last
        if elapsed < self._rate_limit_interval:
            time.sleep(self._rate_limit_interval - elapsed)
        self._rate_limit_last = time.time()

    def _get_cached_coords(self, location: str) -> Optional[Dict]:
        return None

    def _cache_coords(self, location: str, coords: Dict) -> None:
        pass