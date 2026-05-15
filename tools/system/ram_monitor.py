"""
J.A.R.V.I.S. RAM Monitor
Monitors RAM usage and availability.
"""

from typing import Dict, Any

import psutil

from jarvis_core.logger import Logger


class RAMMonitor:
    def __init__(self):
        self.log = Logger("RAMMonitor")
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("RAM monitor ready.")
        return True

    def get_usage(self) -> Dict[str, Any]:
        try:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()

            return {
                "total_gb": round(mem.total / (1024**3), 2),
                "available_gb": round(mem.available / (1024**3), 2),
                "used_gb": round(mem.used / (1024**3), 2),
                "percent": mem.percent,
                "swap_total_gb": round(swap.total / (1024**3), 2),
                "swap_used_gb": round(swap.used / (1024**3), 2),
                "swap_percent": swap.percent,
            }
        except Exception as e:
            self.log.error(f"RAM usage failed: {e}")
            return {"error": str(e)}

    def is_low(self, threshold_percent: int = 90) -> bool:
        usage = self.get_usage()
        return usage.get("percent", 0) >= threshold_percent

    def format_for_voice(self) -> str:
        usage = self.get_usage()
        total = usage.get("total_gb", 0)
        used = usage.get("used_gb", 0)
        percent = usage.get("percent", 0)
        available = usage.get("available_gb", 0)
        return f"RAM usage at {percent} percent. {used:.1f} gigabytes used out of {total:.1f}. {available:.1f} gigabytes available, Sir."