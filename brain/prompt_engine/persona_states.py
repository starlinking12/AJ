"""
J.A.R.V.I.S. Persona States
Manages different personality modes for J.A.R.V.I.S.
"""

from jarvis_core.logger import Logger


class PersonaStates:
    def __init__(self):
        self.log = Logger("PersonaStates")
        self._states = {}
        self._current_state = "default"
        self._load_states()

    def _load_states(self) -> None:
        self._states["default"] = {
            "name": "Default",
            "formality": "high",
            "wit_level": "moderate",
            "speed": "normal",
            "description": "Standard Jarvis personality.",
        }

        self._states["tactical"] = {
            "name": "Tactical",
            "formality": "maximum",
            "wit_level": "none",
            "speed": "fast",
            "description": "Combat mode. No jokes. Pure efficiency.",
        }

        self._states["casual"] = {
            "name": "Casual",
            "formality": "moderate",
            "wit_level": "high",
            "speed": "normal",
            "description": "Relaxed mode. More humor allowed.",
        }

        self._states["stealth"] = {
            "name": "Stealth",
            "formality": "high",
            "wit_level": "none",
            "speed": "fast",
            "volume": "low",
            "description": "Quiet mode. Minimal responses.",
        }

    def set_state(self, state_name: str) -> bool:
        if state_name in self._states:
            self._current_state = state_name
            self.log.info(f"Persona state set to: {state_name}")
            return True
        return False

    def get_current_state(self) -> dict:
        return self._states.get(self._current_state, self._states["default"])

    def get_state_names(self) -> list:
        return list(self._states.keys())

    def get_state_instruction(self) -> str:
        state = self.get_current_state()
        instructions = []

        if state.get("wit_level") == "none":
            instructions.append("Be direct. No humor.")
        elif state.get("wit_level") == "high":
            instructions.append("Witty remarks are encouraged.")

        if state.get("speed") == "fast":
            instructions.append("Keep responses extremely brief.")

        if state.get("volume") == "low":
            instructions.append("Speak quietly. Whisper mode.")

        return " ".join(instructions) if instructions else ""