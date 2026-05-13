"""
J.A.R.V.I.S. Context Transfer
Prepares and transfers context between agents during handoff.
"""

from typing import Dict, Any, Optional

from jarvis_core.logger import Logger


class ContextTransfer:
    def __init__(self):
        self.log = Logger("ContextTransfer")
        self._transfer_protocols: Dict[str, Dict] = {}
        self._load_protocols()

    def _load_protocols(self) -> None:
        self._transfer_protocols["default"] = {
            "include_conversation_history": True,
            "include_user_profile": True,
            "include_active_task": True,
            "max_history_turns": 10,
        }
        self._transfer_protocols["search_to_conversation"] = {
            "include_conversation_history": True,
            "include_user_profile": True,
            "include_active_task": False,
            "include_search_results": True,
            "max_history_turns": 5,
        }
        self._transfer_protocols["system_to_conversation"] = {
            "include_conversation_history": True,
            "include_user_profile": True,
            "include_active_task": False,
            "include_command_result": True,
            "max_history_turns": 5,
        }

    def prepare_transfer(
        self,
        from_agent: str,
        to_agent: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        protocol_key = f"{from_agent}_to_{to_agent}"
        protocol = self._transfer_protocols.get(
            protocol_key,
            self._transfer_protocols["default"]
        )

        package = {
            "from_agent": from_agent,
            "to_agent": to_agent,
            "timestamp": self._get_timestamp(),
        }

        if protocol.get("include_conversation_history"):
            history = context.get("conversation_history", [])
            max_turns = protocol.get("max_history_turns", 10)
            package["conversation_history"] = history[-max_turns:]

        if protocol.get("include_user_profile"):
            package["user_profile"] = context.get("user_profile", {})

        if protocol.get("include_active_task"):
            package["active_task"] = context.get("active_task")

        if protocol.get("include_search_results"):
            package["search_results"] = context.get("search_results")

        if protocol.get("include_command_result"):
            package["command_result"] = context.get("command_result")

        package["custom_context"] = context.get("custom_context", {})
        package["original_query"] = context.get("original_query", "")

        self.log.debug(f"Transfer package prepared: {protocol_key}")
        return package

    def set_protocol(self, from_agent: str, to_agent: str, settings: Dict) -> None:
        key = f"{from_agent}_to_{to_agent}"
        self._transfer_protocols[key] = settings

    def _get_timestamp(self) -> str:
        import time
        return time.strftime("%Y-%m-%dT%H:%M:%S")