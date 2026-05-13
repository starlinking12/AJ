"""
J.A.R.V.I.S. Watchdog
Monitors all services and restarts them if they fail.
"""

import time
import threading
from typing import Dict, Callable

from jarvis_core.logger import Logger


class Watchdog:
    def __init__(self, check_interval: float = 5.0):
        self.check_interval = check_interval
        self.log = Logger("Watchdog")
        self._services: Dict[str, Dict] = {}
        self._running = False
        self._thread: threading.Thread = None

    def register_service(self, name: str, health_check: Callable[[], bool], restart: Callable) -> None:
        self._services[name] = {
            "health_check": health_check,
            "restart": restart,
            "failures": 0,
            "max_failures": 3
        }
        self.log.info(f"Service registered: {name}")

    def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
        self.log.info("Watchdog started.")

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        self.log.info("Watchdog stopped.")

    def _monitor_loop(self) -> None:
        while self._running:
            for name, service in list(self._services.items()):
                try:
                    if not service["health_check"]():
                        service["failures"] += 1
                        self.log.warn(f"Service {name} unhealthy ({service['failures']}/{service['max_failures']})")
                        if service["failures"] >= service["max_failures"]:
                            self.log.error(f"Restarting {name}...")
                            service["restart"]()
                            service["failures"] = 0
                    else:
                        service["failures"] = 0
                except Exception as e:
                    self.log.error(f"Watchdog check failed for {name}: {e}")
            time.sleep(self.check_interval)