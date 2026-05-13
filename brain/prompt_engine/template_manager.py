"""
J.A.R.V.I.S. Template Manager
Manages response templates for common interactions.
"""

from typing import Dict, Optional

from jarvis_core.logger import Logger


class TemplateManager:
    def __init__(self):
        self.log = Logger("TemplateManager")
        self._templates: Dict[str, str] = {}
        self._load_default_templates()

    def _load_default_templates(self) -> None:
        self._templates["greeting_morning"] = "Good morning, Sir. All systems are running optimally."
        self._templates["greeting_afternoon"] = "Good afternoon, Sir. How may I assist?"
        self._templates["greeting_evening"] = "Good evening, Sir. The day's operations are complete."
        self._templates["greeting_night"] = "Late night, Sir. Shall I dim the lights?"
        self._templates["wake"] = "At your service, Sir."
        self._templates["sleep"] = "Going to sleep, Sir. I will be here when you need me."
        self._templates["error"] = "I encountered an issue, Sir. Attempting to recover."
        self._templates["unknown"] = "I am not certain I understood, Sir. Could you rephrase?"
        self._templates["farewell"] = "Until next time, Sir."
        self._templates["task_complete"] = "Task completed, Sir."
        self._templates["task_failed"] = "I was unable to complete that task, Sir."

    def get_template(self, name: str, **kwargs) -> str:
        template = self._templates.get(name, "")
        if template and kwargs:
            template = template.format(**kwargs)
        return template

    def add_template(self, name: str, template: str) -> None:
        self._templates[name] = template
        self.log.info(f"Template added: {name}")

    def remove_template(self, name: str) -> bool:
        if name in self._templates:
            del self._templates[name]
            return True
        return False

    def list_templates(self) -> list:
        return list(self._templates.keys())

    def get_greeting_for_time(self, hour: int) -> str:
        if 5 <= hour < 12:
            return self.get_template("greeting_morning")
        elif 12 <= hour < 17:
            return self.get_template("greeting_afternoon")
        elif 17 <= hour < 22:
            return self.get_template("greeting_evening")
        else:
            return self.get_template("greeting_night")