"""
J.A.R.V.I.S. Tool Registry
Central registry for all available tools. Discovers and manages tool modules.
"""

from typing import Dict, Any, Callable, Optional, List

from jarvis_core.logger import Logger


class ToolRegistry:
    def __init__(self):
        self.log = Logger("ToolRegistry")
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._initialized = False

    def initialize(self) -> bool:
        self._register_builtin_tools()
        self._initialized = True
        self.log.info(f"Tool registry ready. {len(self._tools)} tools registered.")
        return True

    def _register_builtin_tools(self) -> None:
        builtin = [
            {"name": "web_search", "description": "Search the web for information", "category": "search"},
            {"name": "get_news", "description": "Fetch current news headlines", "category": "news"},
            {"name": "get_weather", "description": "Get weather conditions", "category": "weather"},
            {"name": "show_map", "description": "Display interactive maps", "category": "maps"},
            {"name": "city_lookup", "description": "Look up city information", "category": "city"},
            {"name": "system_command", "description": "Execute system commands", "category": "system"},
            {"name": "open_camera", "description": "Open camera feed", "category": "camera"},
            {"name": "play_music", "description": "Play music", "category": "music"},
            {"name": "send_email", "description": "Send emails", "category": "email"},
            {"name": "home_control", "description": "Control smart home devices", "category": "home"},
        ]
        for tool in builtin:
            self._tools[tool["name"]] = {
                "description": tool["description"],
                "category": tool["category"],
                "handler": None,
                "enabled": True,
            }

    def register(self, name: str, description: str, category: str, handler: Callable) -> None:
        self._tools[name] = {
            "description": description,
            "category": category,
            "handler": handler,
            "enabled": True,
        }
        self.log.info(f"Tool registered: {name}")

    def get_tool(self, name: str) -> Optional[Dict]:
        return self._tools.get(name)

    def get_handler(self, name: str) -> Optional[Callable]:
        tool = self._tools.get(name)
        if tool and tool["enabled"]:
            return tool.get("handler")
        return None

    def list_tools(self) -> List[str]:
        return list(self._tools.keys())

    def list_by_category(self, category: str) -> List[str]:
        return [name for name, info in self._tools.items() if info.get("category") == category]

    def is_enabled(self, name: str) -> bool:
        tool = self._tools.get(name)
        return tool is not None and tool.get("enabled", False)

    def enable(self, name: str) -> bool:
        if name in self._tools:
            self._tools[name]["enabled"] = True
            return True
        return False

    def disable(self, name: str) -> bool:
        if name in self._tools:
            self._tools[name]["enabled"] = False
            return True
        return False