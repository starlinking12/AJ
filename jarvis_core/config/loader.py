"""
J.A.R.V.I.S. Config Loader
Loads configuration from YAML files and environment variables.
"""

import os
from pathlib import Path
from typing import Any, Dict

import yaml

from jarvis_core.config.schema import ConfigSchema
from jarvis_core.config.env_loader import EnvLoader
from jarvis_core.logger import Logger


class Config:
    def __init__(self, data: Dict[str, Any]):
        self._data = data
        for key, value in data.items():
            setattr(self, key, value)

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    @classmethod
    def load(cls, config_dir: str = None) -> "Config":
        log = Logger("Config")

        if config_dir is None:
            config_dir = Path(__file__).resolve().parent

        defaults_path = Path(config_dir) / "defaults.yaml"
        user_path = Path(config_dir) / "user_config.yaml"

        data = {}

        if defaults_path.exists():
            with open(defaults_path, "r") as f:
                data = yaml.safe_load(f) or {}
            log.info(f"Loaded defaults from {defaults_path}")

        if user_path.exists():
            with open(user_path, "r") as f:
                user_data = yaml.safe_load(f) or {}
            data.update(user_data)
            log.info(f"Loaded user config from {user_path}")

        env_data = EnvLoader.load()
        data.update(env_data)

        schema = ConfigSchema(data)
        validated = schema.validate()

        return cls(validated)