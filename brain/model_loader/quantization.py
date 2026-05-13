"""
J.A.R.V.I.S. Quantization Manager
Handles model quantization settings for performance optimization.
"""

from typing import Optional

from jarvis_core.logger import Logger


class QuantizationManager:
    def __init__(self):
        self.log = Logger("Quantization")
        self._quantization_levels = {
            "q4_0": {"bits": 4, "quality": "good", "speed": "fastest"},
            "q4_1": {"bits": 4, "quality": "better", "speed": "fast"},
            "q5_0": {"bits": 5, "quality": "better", "speed": "fast"},
            "q5_1": {"bits": 5, "quality": "best", "speed": "medium"},
            "q8_0": {"bits": 8, "quality": "best", "speed": "medium"},
            "f16": {"bits": 16, "quality": "maximum", "speed": "slow"},
        }
        self._current_level = "q4_0"

    def set_level(self, level: str) -> bool:
        if level in self._quantization_levels:
            self._current_level = level
            self.log.info(f"Quantization set to {level}")
            return True
        return False

    def get_current_config(self) -> dict:
        return self._quantization_levels.get(self._current_level, {})

    def get_level_for_hardware(self, ram_gb: int, has_gpu: bool = False) -> str:
        if has_gpu and ram_gb >= 16:
            return "q8_0"
        elif ram_gb >= 16:
            return "q5_1"
        elif ram_gb >= 8:
            return "q4_1"
        else:
            return "q4_0"

    def list_levels(self) -> list:
        return list(self._quantization_levels.keys())