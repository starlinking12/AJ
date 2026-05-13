"""
J.A.R.V.I.S. Tool Schema
Defines parameter schemas for all tools.
"""

from typing import Dict, Any, List


class ToolSchema:
    def __init__(self):
        self._schemas: Dict[str, Dict] = {}
        self._load_schemas()

    def _load_schemas(self) -> None:
        self._schemas = {
            "web_search": {
                "parameters": {
                    "query": {"type": "str", "required": True, "description": "Search query"},
                    "depth": {"type": "str", "required": False, "default": "quick", "options": ["quick", "deep"]},
                    "max_results": {"type": "int", "required": False, "default": 5},
                }
            },
            "get_news": {
                "parameters": {
                    "category": {"type": "str", "required": False, "default": "all"},
                    "limit": {"type": "int", "required": False, "default": 10},
                    "country": {"type": "str", "required": False, "default": "us"},
                }
            },
            "get_weather": {
                "parameters": {
                    "location": {"type": "str", "required": True, "description": "City name or coordinates"},
                    "units": {"type": "str", "required": False, "default": "celsius", "options": ["celsius", "fahrenheit"]},
                }
            },
            "show_map": {
                "parameters": {
                    "location": {"type": "str", "required": True, "description": "Place to display"},
                    "zoom": {"type": "int", "required": False, "default": 13},
                }
            },
            "city_lookup": {
                "parameters": {
                    "city": {"type": "str", "required": True, "description": "City name"},
                    "country": {"type": "str", "required": False},
                }
            },
            "system_command": {
                "parameters": {
                    "command": {"type": "str", "required": True, "description": "Command to execute"},
                    "app": {"type": "str", "required": False, "description": "Application name to open"},
                }
            },
            "open_camera": {
                "parameters": {}
            },
            "play_music": {
                "parameters": {
                    "query": {"type": "str", "required": True, "description": "Song, artist, or playlist"},
                    "source": {"type": "str", "required": False, "default": "spotify", "options": ["spotify", "youtube", "local"]},
                }
            },
            "send_email": {
                "parameters": {
                    "to": {"type": "str", "required": True},
                    "subject": {"type": "str", "required": True},
                    "body": {"type": "str", "required": True},
                }
            },
            "home_control": {
                "parameters": {
                    "device": {"type": "str", "required": True, "description": "Device name or type"},
                    "action": {"type": "str", "required": True, "description": "Action to perform"},
                    "value": {"type": "str", "required": False},
                }
            },
        }

    def get_schema(self, tool_name: str) -> Dict:
        return self._schemas.get(tool_name, {})

    def validate_params(self, tool_name: str, params: Dict) -> Dict[str, Any]:
        schema = self.get_schema(tool_name)
        if not schema:
            return {"valid": True, "errors": []}

        errors = []
        param_schemas = schema.get("parameters", {})

        for param_name, param_schema in param_schemas.items():
            if param_schema.get("required") and param_name not in params:
                errors.append(f"Missing required parameter: {param_name}")

        if params:
            for param_name, value in params.items():
                if param_name in param_schemas:
                    expected_type = param_schema.get("type")
                    if expected_type == "str" and not isinstance(value, str):
                        errors.append(f"Parameter {param_name} must be a string")
                    elif expected_type == "int" and not isinstance(value, int):
                        errors.append(f"Parameter {param_name} must be an integer")

        return {"valid": len(errors) == 0, "errors": errors}

    def get_all_schemas(self) -> Dict:
        return self._schemas