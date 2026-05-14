"""
J.A.R.V.I.S. Distance Matrix
Calculates distances between multiple points.
"""

from typing import Dict, Any, List, Optional

import requests

from jarvis_core.logger import Logger


class DistanceMatrix:
    def __init__(self):
        self.log = Logger("DistanceMatrix")
        self.base_url = "https://router.project-osrm.org/table/v1/driving"
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("Distance matrix ready (OSRM).")
        return True

    def calculate(
        self,
        points: List[Dict[str, float]]
    ) -> Optional[Dict[str, Any]]:
        if not self._initialized or len(points) < 2:
            return None

        try:
            coord_strings = [f"{p['lng']},{p['lat']}" for p in points]
            coords = ";".join(coord_strings)

            params = {"annotations": "distance,duration"}

            response = requests.get(
                f"{self.base_url}/{coords}",
                params=params,
                timeout=15
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "distances": data.get("distances", []),
                    "durations": data.get("durations", []),
                    "sources": data.get("sources", []),
                    "destinations": data.get("destinations", []),
                }

            return None

        except Exception as e:
            self.log.error(f"Distance matrix failed: {e}")
            return None

    def get_distance(
        self,
        origin: Dict[str, float],
        destination: Dict[str, float]
    ) -> Optional[float]:
        result = self.calculate([origin, destination])
        if result and result.get("distances"):
            distances = result["distances"]
            if len(distances) > 0 and len(distances[0]) > 1:
                return distances[0][1] / 1000
        return None