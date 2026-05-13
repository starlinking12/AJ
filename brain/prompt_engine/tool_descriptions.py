"""
J.A.R.V.I.S. Tool Descriptions
Describes available tools for the LLM to use.
"""

from typing import List, Dict

from jarvis_core.logger import Logger


class ToolDescriptions:
    def __init__(self):
        self.log = Logger("ToolDescriptions")
        self._tools: List[Dict] = []
        self._load_default_tools()

    def _load_default_tools(self) -> None:
        self._tools = [
            {
                "name": "web_search",
                "description": "Search the web for information. Returns summarized results with sources.",
                "parameters": {
                    "query": "The search query string",
                    "depth": "Search depth: 'quick' or 'deep'",
                }
            },
            {
                "name": "get_news",
                "description": "Fetch current news headlines. Can filter by category.",
                "parameters": {
                    "category": "News category: technology, science, world, business, or all",
                    "limit": "Number of articles to return (default: 10)",
                }
            },
            {
                "name": "get_weather",
                "description": "Get current weather conditions and forecast.",
                "parameters": {
                    "location": "City name or coordinates",
                    "units": "Temperature units: 'celsius' or 'fahrenheit'",
                }
            },
            {
                "name": "show_map",
                "description": "Display an interactive map on screen.",
                "parameters": {
                    "location": "Place name, address, or coordinates to display",
                    "zoom": "Map zoom level (1-18)",
                }
            },
            {
                "name": "open_camera",
                "description": "Open the camera feed on screen.",
                "parameters": {}
            },
            {
                "name": "close_camera",
                "description": "Close the camera feed.",
                "parameters": {}
            },
            {
                "name": "system_command",
                "description": "Execute a system command on the computer.",
                "parameters": {
                    "command": "The system command to execute",
                    "app": "Application name to open",
                }
            },
            {
                "name": "play_music",
                "description": "Play music from available sources.",
                "parameters": {
                    "query": "Song name, artist, or playlist",
                }
            },
        ]

    def get_tool_list(self) -> List[Dict]:
        return self._tools

    def get_tool_names(self) -> List[str]:
        return [t["name"] for t in self._tools]

    def get_tool_description(self, tool_name: str) -> str:
        for tool in self._tools:
            if tool["name"] == tool_name:
                params = tool.get("parameters", {})
                param_str = ", ".join(f"{k}: {v}" for k, v in params.items())
                return f"{tool['name']}: {tool['description']}. Parameters: {param_str}"
        return ""

    def get_formatted_for_prompt(self) -> str:
        lines = ["Available tools:"]
        for tool in self._tools:
            lines.append(f"- {self.get_tool_description(tool['name'])}")
        return "\n".join(lines)

    def add_tool(self, name: str, description: str, parameters: Dict = None) -> None:
        self._tools.append({
            "name": name,
            "description": description,
            "parameters": parameters or {},
        })