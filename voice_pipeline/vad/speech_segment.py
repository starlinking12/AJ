"""
J.A.R.V.I.S. Speech Segment
Represents a detected speech segment with metadata.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SpeechSegment:
    audio_data: bytes
    sample_rate: int = 16000
    duration_ms: float = 0.0
    start_time: float = 0.0
    end_time: float = 0.0
    energy_level: float = 0.0
    is_speech: bool = True
    metadata: dict = field(default_factory=dict)

    @property
    def duration_seconds(self) -> float:
        return self.duration_ms / 1000.0

    def is_valid(self) -> bool:
        return len(self.audio_data) > 0 and self.duration_ms > 0

    def is_too_short(self, min_duration_ms: float = 200.0) -> bool:
        return self.duration_ms < min_duration_ms

    def is_too_long(self, max_duration_ms: float = 30000.0) -> bool:
        return self.duration_ms > max_duration_ms