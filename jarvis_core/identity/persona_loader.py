"""
J.A.R.V.I.S. Persona Loader
Loads the J.A.R.V.I.S. personality profile.
"""

import json
from pathlib import Path
from typing import Dict

from jarvis_core.logger import Logger


class Persona:
    def __init__(self):
        self.log = Logger("Persona")
        self.data: Dict = {}
        self._load()

    def _load(self) -> None:
        identity_dir = Path(__file__).resolve().parent

        backstory_path = identity_dir / "backstory.json"
        if backstory_path.exists():
            with open(backstory_path, "r") as f:
                self.data["backstory"] = json.load(f)

        greetings_path = identity_dir / "greetings.json"
        if greetings_path.exists():
            with open(greetings_path, "r") as f:
                self.data["greetings"] = json.load(f)

        self.log.info("Persona loaded.")

    def get_backstory(self) -> Dict:
        return self.data.get("backstory", {})

    def get_greeting(self, time_of_day: str = "general") -> str:
        greetings = self.data.get("greetings", {})
        return greetings.get(time_of_day, greetings.get("general", "At your service, Sir."))