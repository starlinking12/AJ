"""
J.A.R.V.I.S. Tool Executor
Executes tool commands with error handling and timeout protection.
"""

import time
from typing import Dict, Any, Optional

from tools.tool_registry import ToolRegistry
from jarvis_core.logger import Logger
from jarvis_core.events.event_bus import EventBus


class ToolExecutor:
    def __init__(self, registry: ToolRegistry, event_bus: EventBus):
        self.log = Logger("ToolExecutor")
        self.registry = registry
        self.event_bus = event_bus
        self._default_timeout = 30
        self._execution_history: list = []

    def execute(self, tool_name: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        if params is None:
            params = {}

        handler = self.registry.get_handler(tool_name)
        if handler is None:
            return {
                "success": False,
                "error": f"Tool not found or disabled: {tool_name}",
                "data": None,
            }

        start_time = time.time()
        self.event_bus.emit("tool.execution.started", {"tool": tool_name, "params": params})

        try:
            result = handler(params)
            elapsed = time.time() - start_time

            self._execution_history.append({
                "tool": tool_name,
                "params": params,
                "success": True,
                "elapsed_ms": int(elapsed * 1000),
                "timestamp": time.time(),
            })

            self.event_bus.emit("tool.execution.complete", {
                "tool": tool_name,
                "success": True,
                "elapsed_ms": int(elapsed * 1000),
            })

            return {
                "success": True,
                "data": result,
                "elapsed_ms": int(elapsed * 1000),
                "tool": tool_name,
            }

        except Exception as e:
            elapsed = time.time() - start_time
            self.log.error(f"Tool execution failed: {tool_name} - {e}")

            self._execution_history.append({
                "tool": tool_name,
                "params": params,
                "success": False,
                "error": str(e),
                "elapsed_ms": int(elapsed * 1000),
                "timestamp": time.time(),
            })

            self.event_bus.emit("tool.execution.failed", {
                "tool": tool_name,
                "error": str(e),
            })

            return {
                "success": False,
                "error": str(e),
                "data": None,
                "tool": tool_name,
            }

    def get_history(self, limit: int = 20) -> list:
        return self._execution_history[-limit:]

    def clear_history(self) -> None:
        self._execution_history = []