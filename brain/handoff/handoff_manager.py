"""
J.A.R.V.I.S. Handoff Manager
Manages sequential agent handoffs without context loss.
Enables customer-support-grade context preservation across agent boundaries.
"""

from typing import Dict, Any, Optional, Callable

from brain.handoff.agent_bridge import AgentBridge
from brain.handoff.context_transfer import ContextTransfer
from brain.handoff.state_serializer import StateSerializer

from jarvis_core.logger import Logger
from jarvis_core.events.event_bus import EventBus


class HandoffManager:
    """
    Coordinates handoffs between specialized agents.
    Preserves full conversation context when switching domains.
    """

    def __init__(self, event_bus: EventBus):
        self.log = Logger("HandoffManager")
        self.event_bus = event_bus
        self.bridge = AgentBridge()
        self.context_transfer = ContextTransfer()
        self.state_serializer = StateSerializer()
        self._current_agent: Optional[str] = None
        self._agent_states: Dict[str, Dict] = {}
        self._handoff_history: list = []

    def register_agent(self, agent_name: str, handler: Callable) -> None:
        self.bridge.register(agent_name, handler)
        self._agent_states[agent_name] = {"status": "idle", "last_active": None}
        self.log.info(f"Agent registered: {agent_name}")

    def handoff(
        self,
        from_agent: str,
        to_agent: str,
        context: Dict[str, Any],
        reason: str = ""
    ) -> bool:
        if not self.bridge.is_registered(to_agent):
            self.log.error(f"Target agent not registered: {to_agent}")
            return False

        self.log.info(f"Handoff: {from_agent} -> {to_agent}. Reason: {reason}")

        transfer_package = self.context_transfer.prepare_transfer(
            from_agent=from_agent,
            to_agent=to_agent,
            context=context
        )

        self.state_serializer.save_state(from_agent, self._agent_states.get(from_agent, {}))

        success = self.bridge.transfer(to_agent, transfer_package)

        if success:
            self._current_agent = to_agent
            self._agent_states[to_agent] = {
                "status": "active",
                "last_active": self._get_timestamp(),
                "context": transfer_package,
            }
            self._agent_states[from_agent] = {
                "status": "idle",
                "last_active": self._get_timestamp(),
            }

            self._handoff_history.append({
                "from": from_agent,
                "to": to_agent,
                "reason": reason,
                "timestamp": self._get_timestamp(),
            })

            self.event_bus.emit("handoff.completed", {
                "from": from_agent,
                "to": to_agent,
                "reason": reason,
            })

        return success

    def get_current_agent(self) -> Optional[str]:
        return self._current_agent

    def get_agent_state(self, agent_name: str) -> Dict:
        return self._agent_states.get(agent_name, {"status": "unknown"})

    def get_handoff_history(self, limit: int = 10) -> list:
        return self._handoff_history[-limit:]

    def _get_timestamp(self) -> str:
        import time
        return time.strftime("%Y-%m-%dT%H:%M:%S")