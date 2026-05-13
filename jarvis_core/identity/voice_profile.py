"""
J.A.R.V.I.S. Voice Profile
Defines the voice characteristics for J.A.R.V.I.S.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class VoiceProfile:
    engine: str = "piper"
    model: str = "jarvis_british_male"
    language: str = "en_GB"
    speed: float = 1.0
    pitch: float = 1.0
    volume: float = 1.0
    sample_rate: int = 22050

    # Voice cloning
    rvc_model_path: Optional[str] = None
    xtts_model_path: Optional[str] = None

    # Audio post-processing
    highpass_filter: Optional[float] = 200.0
    treble_boost: Optional[float] = 6.0
    echo_amount: Optional[float] = 0.1


DEFAULT_JARVIS_VOICE = VoiceProfile(
    engine="piper",
    model="jarvis_british_male",
    language="en_GB",
    speed=1.0,
    pitch=1.0,
    volume=1.0,
)