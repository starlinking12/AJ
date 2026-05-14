"""
J.A.R.V.I.S. NOAA Client
Uses NOAA API for US weather data.
Free. No API key required for basic endpoints.
"""

from typing import Dict, Any, Optional

import requests

from jarvis_core.logger import Logger


class NOAAClient:
    def __init__(self):
        self.log = Logger("NOAAClient")
        self.base_url = "https://api.weather.gov"
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("NOAA client ready (free, US-focused).")
        return True

    def get_current(self, location: str, units: str = "celsius") -> Dict[str, Any]:
        return {"error": "NOAA requires coordinates. Use Open-Meteo for location search."}

    def get_forecast(self, location: str, days: int = 7, units: str = "celsius") -> Dict[str, Any]:
        return {"error": "NOAA requires coordinates. Use Open-Meteo for location search."}

    def get_by_coordinates(self, lat: float, lng: float) -> Optional[Dict[str, Any]]:
        try:
            headers = {"User-Agent": "JARVIS/1.0", "Accept": "application/json"}

            points_response = requests.get(
                f"{self.base_url}/points/{lat},{lng}",
                headers=headers,
                timeout=10
            )

            if points_response.status_code != 200:
                return None

            points_data = points_response.json()
            forecast_url = points_data.get("properties", {}).get("forecast")

            if not forecast_url:
                return None

            forecast_response = requests.get(forecast_url, headers=headers, timeout=10)

            if forecast_response.status_code == 200:
                forecast_data = forecast_response.json()
                periods = forecast_data.get("properties", {}).get("periods", [])

                if periods:
                    current = periods[0]
                    return {
                        "temperature": current.get("temperature"),
                        "feels_like": current.get("temperature"),
                        "condition": current.get("shortForecast", ""),
                        "wind_speed": current.get("windSpeed", ""),
                        "wind_direction": current.get("windDirection", ""),
                        "humidity": current.get("relativeHumidity", {}).get("value") if current.get("relativeHumidity") else None,
                        "source": "noaa",
                    }

            return None

        except Exception as e:
            self.log.error(f"NOAA request failed: {e}")
            return None