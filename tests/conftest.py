"""
J.A.R.V.I.S. Test Configuration
Shared fixtures for all tests.
"""

import os
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

os.environ["JARVIS_TEST_MODE"] = "true"


@pytest.fixture
def sample_config():
    from jarvis_core.config.loader import Config
    return Config.load()


@pytest.fixture
def event_bus():
    from jarvis_core.events.event_bus import EventBus
    return EventBus()


@pytest.fixture
def sample_audio_bytes():
    import struct
    import math
    sample_rate = 16000
    duration = 1.0
    frequency = 440.0
    samples = []
    for i in range(int(sample_rate * duration)):
        value = int(16000 * math.sin(2 * math.pi * frequency * i / sample_rate))
        samples.append(value)
    return struct.pack("h" * len(samples), *samples)


@pytest.fixture
def sample_text():
    return "What is the weather in London today?"


@pytest.fixture
def mock_llm_response():
    return "Current conditions in London show 15 degrees Celsius with light rain, Sir."