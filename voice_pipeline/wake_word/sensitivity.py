"""
J.A.R.V.I.S. Wake Word Sensitivity
Manages wake word detection sensitivity levels.
"""

from jarvis_core.logger import Logger


class Sensitivity:
    def __init__(self, initial: float = 0.5):
        self.log = Logger("Sensitivity")
        self._value = self._clamp(initial)
        self._min = 0.1
        self._max = 0.9

    @property
    def value(self) -> float:
        return self._value

    def set(self, new_value: float) -> None:
        self._value = self._clamp(new_value)
        self.log.info(f"Sensitivity set to {self._value}")

    def increase(self, step: float = 0.1) -> float:
        self._value = self._clamp(self._value + step)
        return self._value

    def decrease(self, step: float = 0.1) -> float:
        self._value = self._clamp(self._value - step)
        return self._value

    def _clamp(self, value: float) -> float:
        return max(self._min, min(self._max, value))

    def to_description(self) -> str:
        if self._value <= 0.3:
            return "Low - requires clear pronunciation, fewer false triggers"
        elif self._value <= 0.5:
            return "Medium - balanced detection"
        elif self._value <= 0.7:
            return "High - sensitive, may trigger on similar sounds"
        else:
            return "Very High - maximum sensitivity, may have false triggers"