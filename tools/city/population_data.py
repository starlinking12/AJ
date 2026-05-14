"""
J.A.R.V.I.S. Population Data
Formats population numbers for voice delivery.
"""

from typing import Optional

from jarvis_core.logger import Logger


class PopulationData:
    def __init__(self):
        self.log = Logger("PopulationData")

    def format_population(self, population: int) -> str:
        if population >= 1000000000:
            return f"{population / 1000000000:.2f} billion"
        elif population >= 1000000:
            return f"{population / 1000000:.1f} million"
        elif population >= 1000:
            return f"{population / 1000:.1f} thousand"
        else:
            return str(population)

    def classify_size(self, population: int) -> str:
        if population >= 10000000:
            return "megacity"
        elif population >= 1000000:
            return "large city"
        elif population >= 100000:
            return "medium city"
        elif population >= 10000:
            return "small city"
        elif population >= 1000:
            return "town"
        else:
            return "village"

    def get_population_density_label(self, density_per_km2: float) -> str:
        if density_per_km2 >= 20000:
            return "extremely dense"
        elif density_per_km2 >= 10000:
            return "very dense"
        elif density_per_km2 >= 5000:
            return "dense"
        elif density_per_km2 >= 1000:
            return "moderate"
        elif density_per_km2 >= 100:
            return "sparse"
        else:
            return "very sparse"