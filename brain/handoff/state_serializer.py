"""
J.A.R.V.I.S. State Serializer
Serializes and deserializes agent state for persistence and recovery.
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, Optional

from jarvis_core.logger import Logger


class StateSerializer:
    def __init__(self, storage_dir: str = None):
        self.log = Logger("StateSerializer")
        if storage_dir is None:
            storage_dir = Path(__file__).resolve().parent.parent.parent / "data" / "agent_states"
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save_state(self, agent_name: str, state: Dict[str, Any]) -> bool:
        try:
            state_file = self.storage_dir / f"{agent_name}_state.json"
            serializable = self._make_serializable(state)
            serializable["_saved_at"] = time.time()

            with open(state_file, "w") as f:
                json.dump(serializable, f, indent=2)

            self.log.debug(f"State saved: {agent_name}")
            return True

        except Exception as e:
            self.log.error(f"Failed to save state for {agent_name}: {e}")
            return False

    def load_state(self, agent_name: str) -> Optional[Dict[str, Any]]:
        try:
            state_file = self.storage_dir / f"{agent_name}_state.json"
            if not state_file.exists():
                return None

            with open(state_file, "r") as f:
                state = json.load(f)

            self.log.debug(f"State loaded: {agent_name}")
            return state

        except Exception as e:
            self.log.error(f"Failed to load state for {agent_name}: {e}")
            return None

    def delete_state(self, agent_name: str) -> bool:
        try:
            state_file = self.storage_dir / f"{agent_name}_state.json"
            if state_file.exists():
                state_file.unlink()
                return True
            return False
        except Exception as e:
            self.log.error(f"Failed to delete state for {agent_name}: {e}")
            return False

    def list_saved_states(self) -> list:
        return [
            f.stem.replace("_state", "")
            for f in self.storage_dir.glob("*_state.json")
        ]

    def _make_serializable(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        elif isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        else:
            return str(obj)