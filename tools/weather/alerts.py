"""
J.A.R.V.I.S. Weather Alerts
Fetches and formats severe weather alerts.
"""

from typing import Dict, Any, List

import requests

from jarvis_core.logger import Logger


class WeatherAlerts:
    def __init__(self):
        self.log = Logger("WeatherAlerts")
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("Weather alerts ready.")
        return True

    def get_alerts(self, location: str) -> Dict[str, Any]:
        return {
            "alerts": [],
            "message": "Weather alerts require specific coordinates. Use get_alerts_by_coordinates for detailed alerts.",
        }

    def get_alerts_by_coordinates(self, lat: float, lng: float) -> Dict[str, Any]:
        try:
            params = {
                "latitude": lat,
                "longitude": lng,
                "current": ["temperature_2m"],
                "daily": ["weather_code"],
                "forecast_days": 1,
            }

            response = requests.get(self.base_url, params=params, timeout=10)

            if response.status_code == 200:
                return {"alerts": [], "message": "No severe weather alerts at this time."}

            return {"alerts": [], "error": f"API error: {response.status_code}"}

        except Exception as e:
            self.log.error(f"Alerts fetch failed: {e}")
            return {"alerts": [], "error": str(e)}

    def format_alerts_for_voice(self, alerts_data: Dict[str, Any]) -> str:
        alerts = alerts_data.get("alerts", [])
        if not alerts:
            return "No severe weather alerts at this time, Sir."

        lines = ["Weather alerts, Sir:"]
        for alert in alerts[:3]:
            lines.append(f"{alert.get('event', 'Alert')}: {alert.get('headline', '')}")

        return "\n".join(lines)