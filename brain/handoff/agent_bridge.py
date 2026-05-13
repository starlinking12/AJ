"""
J.A.R.V.I.S. Agent Bridge
Connects agents and enables seamless transfers between them.
"""

from typing import Dict, Any, Callable, Optional

from jarvis_core.logger import Logger


class AgentBridge:
    def __init__(self):
        self.log = Logger("AgentBridge")
        self._agents: Dict[str, Dict] = {}
        self._active_connections: Dict[str, str] = {}

    def register(self, agent_name: str, handler: Callable) -> None:
        self._agents[agent_name] = {
            "handler": handler,
            "status": "registered",
            "connections": [],
        }
        self.log.info(f"Bridge: agent '{agent_name}' registered.")

    def unregister(self, agent_name: str) -> bool:
        if agent_name in self._agents:
            del self._agents[agent_name]
            self._active_connections = {
                k: v for k, v in self._active_connections.items()
                if v != agent_name and k != agent_name
            }
            return True
        return False

    def transfer(self, target_agent: str, data: Dict[str, Any]) -> bool:
        if target_agent not in self._agents:
            self.log.error(f"Transfer failed: '{target_agent}' not registered.")
            return False

        try:
            agent = self._agents[target_agent]
            handler = agent["handler"]

            if callable(handler):
                handler(data)
                self.log.info(f"Transfer to '{target_agent}' successful.")
                return True

            self.log.error(f"Handler for '{target_agent}' is not callable.")
            return False

        except Exception as e:
            self.log.error(f"Transfer to '{target_agent}' failed: {e}")
            return False

    def connect(self, agent_a: str, agent_b: str) -> None:
        if agent_a in self._agents and agent_b in self._agents:
            if agent_b not in self._agents[agent_a]["connections"]:
                self._agents[agent_a]["connections"].append(agent_b)
            if agent_a not in self._agents[agent_b]["connections"]:
                self._agents[agent_b]["connections"].append(agent_a)

    def is_registered(self, agent_name: str) -> bool:
        return agent_name in self._agents

    def get_registered_agents(self) -> list:
        return list(self._agents.keys())

    def get_connections(self, agent_name: str) -> list:
        if agent_name in self._agents:
            return self._agents[agent_name]["connections"]
        return []