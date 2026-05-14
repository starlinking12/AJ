"""
J.A.R.V.I.S. Route Planner
Plans routes between two points using OSRM.
Free, no API key required.
"""

from typing import Dict, Any, Optional, List

import requests

from jarvis_core.logger import Logger


class RoutePlanner:
    def __init__(self):
        self.log = Logger("RoutePlanner")
        self.base_url = "https://router.project-osrm.org/route/v1/driving"
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("Route planner ready (OSRM).")
        return True

    def plan(
        self,
        origin_lat: float,
        origin_lng: float,
        dest_lat: float,
        dest_lng: float
    ) -> Optional[Dict[str, Any]]:
        if not self._initialized:
            return None

        try:
            coords = f"{origin_lng},{origin_lat};{dest_lng},{dest_lat}"
            params = {
                "overview": "full",
                "geometries": "geojson",
                "steps": "true",
            }

            response = requests.get(
                f"{self.base_url}/{coords}",
                params=params,
                timeout=15
            )

            if response.status_code == 200:
                data = response.json()
                routes = data.get("routes", [])
                if routes:
                    route = routes[0]
                    return {
                        "distance_km": round(route.get("distance", 0) / 1000, 2),
                        "duration_minutes": round(route.get("duration", 0) / 60, 1),
                        "geometry": route.get("geometry", {}),
                        "steps": self._extract_steps(route),
                        "origin": {"lat": origin_lat, "lng": origin_lng},
                        "destination": {"lat": dest_lat, "lng": dest_lng},
                    }

            return None

        except Exception as e:
            self.log.error(f"Route planning failed: {e}")
            return None

    def _extract_steps(self, route: Dict) -> List[str]:
        steps = []
        for leg in route.get("legs", []):
            for step in leg.get("steps", []):
                instruction = step.get("name", "") or step.get("ref", "")
                if not instruction:
                    instruction = step.get("maneuver", {}).get("type", "Continue")
                distance = round(step.get("distance", 0))
                if distance > 0:
                    instruction += f" ({distance}m)"
                steps.append(instruction)
        return steps