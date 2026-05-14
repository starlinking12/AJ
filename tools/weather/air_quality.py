"""
J.A.R.V.I.S. Air Quality
Fetches air quality data using Open-Meteo Air Quality API.
Free. No API key required.
"""

from typing import Dict, Any, Optional

import requests

from jarvis_core.logger import Logger


class AirQuality:
    def __init__(self):
        self.log = Logger("AirQuality")
        self.base_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("Air quality module ready.")
        return True

    def get(self, location: str) -> Dict[str, Any]:
        return {"message": "Air quality requires coordinates.", "data": None}

    def get_by_coordinates(self, lat: float, lng: float) -> Optional[Dict[str, Any]]:
        try:
            params = {
                "latitude": lat,
                "longitude": lng,
                "current": [
                    "european_aqi",
                    "pm2_5",
                    "pm10",
                    "nitrogen_dioxide",
                    "ozone",
                ],
            }

            response = requests.get(self.base_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                current = data.get("current", {})

                aqi = current.get("european_aqi", 0)
                if isinstance(aqi, list) and len(aqi) > 0:
                    aqi = aqi[0]

                return {
                    "aqi": aqi,
                    "level": self._aqi_to_level(aqi),
                    "pm2_5": current.get("pm2_5", [None])[0] if current.get("pm2_5") else None,
                    "pm10": current.get("pm10", [None])[0] if current.get("pm10") else None,
                    "source": "open-meteo",
                }

            return None

        except Exception as e:
            self.log.error(f"Air quality fetch failed: {e}")
            return None

    def _aqi_to_level(self, aqi: int) -> str:
        if aqi <= 20:
            return "Good"
        elif aqi <= 40:
            return "Fair"
        elif aqi <= 60:
            return "Moderate"
        elif aqi <= 80:
            return "Poor"
        elif aqi <= 100:
            return "Very Poor"
        else:
            return "Extremely Poor"

    def format_for_voice(self, data: Dict[str, Any]) -> str:
        if not data or data.get("aqi") is None:
            return "Air quality data unavailable, Sir."

        aqi = data.get("aqi", 0)
        level = data.get("level", "Unknown")
        return f"Air quality is {level} with an index of {aqi}, Sir."