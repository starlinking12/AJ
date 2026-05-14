"""
J.A.R.V.I.S. Current Conditions
Formats current weather data for voice delivery.
"""

from typing import Dict, Any

from jarvis_core.logger import Logger


class CurrentConditions:
    def __init__(self):
        self.log = Logger("CurrentConditions")

    def format_for_voice(self, data: Dict[str, Any]) -> str:
        if data.get("error"):
            return f"I am unable to fetch the weather at the moment, Sir. {data['error']}"

        location = data.get("location", "your location")
        temp = data.get("temperature")
        condition = data.get("condition", "unknown conditions")
        feels_like = data.get("feels_like")
        humidity = data.get("humidity")
        wind_speed = data.get("wind_speed")
        units = data.get("units", "celsius")
        unit_symbol = "C" if units == "celsius" else "F"

        parts = [f"Currently in {location}"]

        if temp is not None:
            parts.append(f"{temp} degrees {unit_symbol}")

        if condition:
            parts.append(f"with {condition.lower()}")

        if feels_like is not None and feels_like != temp:
            parts.append(f"Feels like {feels_like} degrees")

        if humidity is not None:
            parts.append(f"Humidity at {humidity} percent")

        if wind_speed is not None:
            parts.append(f"Wind speed {wind_speed} kilometers per hour")

        return ", ".join(parts) + ", Sir."

    def get_icon_suggestion(self, weather_code: int) -> str:
        if weather_code == 0:
            return "sunny"
        elif weather_code <= 2:
            return "partly_cloudy"
        elif weather_code == 3:
            return "cloudy"
        elif weather_code <= 48:
            return "fog"
        elif weather_code <= 55:
            return "drizzle"
        elif weather_code <= 65:
            return "rain"
        elif weather_code <= 75:
            return "snow"
        elif weather_code <= 82:
            return "showers"
        elif weather_code >= 95:
            return "thunderstorm"
        return "unknown"