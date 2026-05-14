"""
J.A.R.V.I.S. Weather Forecast
Formats weather forecast data for voice delivery.
"""

from typing import Dict, Any, List

from jarvis_core.logger import Logger


class Forecast:
    def __init__(self):
        self.log = Logger("Forecast")

    def format_for_voice(self, data: Dict[str, Any], days: int = 3) -> str:
        if data.get("error"):
            return f"Forecast unavailable, Sir. {data['error']}"

        location = data.get("location", "your location")
        daily = data.get("daily", [])
        units = data.get("units", "celsius")
        unit_symbol = "C" if units == "celsius" else "F"

        if not daily:
            return f"No forecast data available for {location}, Sir."

        lines = [f"Forecast for {location}, Sir."]

        for day in daily[:days]:
            date = day.get("date", "")
            temp_max = day.get("temp_max")
            temp_min = day.get("temp_min")
            condition = day.get("condition", "")

            day_str = f"{date}: {condition}"

            if temp_max is not None and temp_min is not None:
                day_str += f", high of {temp_max} degrees {unit_symbol}"
                day_str += f", low of {temp_min} degrees {unit_symbol}"

            lines.append(day_str)

        if len(daily) > days:
            lines.append(f"And {len(daily) - days} more days available, Sir.")

        return "\n".join(lines)

    def get_trend(self, daily: List[Dict]) -> str:
        if len(daily) < 2:
            return "Not enough data for trend analysis."

        today_temp = daily[0].get("temp_max", 0)
        tomorrow_temp = daily[1].get("temp_max", 0)

        diff = tomorrow_temp - today_temp

        if diff > 3:
            return "Warming trend expected."
        elif diff < -3:
            return "Cooling trend expected."
        else:
            return "Temperatures expected to remain stable."