"""
J.A.R.V.I.S. CPU Monitor
Monitors CPU usage, frequency, and temperature.
"""

from typing import Dict, Any

import psutil

from jarvis_core.logger import Logger


class CPUMonitor:
    def __init__(self):
        self.log = Logger("CPUMonitor")
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("CPU monitor ready.")
        return True

    def get_usage(self) -> Dict[str, Any]:
        try:
            cpu_percent = psutil.cpu_percent(interval=0.5)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()

            return {
                "percent": cpu_percent,
                "cores": cpu_count,
                "frequency_mhz": round(cpu_freq.current, 0) if cpu_freq else None,
            }
        except Exception as e:
            self.log.error(f"CPU usage failed: {e}")
            return {"error": str(e)}

    def get_per_core_usage(self) -> list:
        try:
            percents = psutil.cpu_percent(interval=0.5, percpu=True)
            return [
                {"core": i, "percent": p}
                for i, p in enumerate(percents)
            ]
        except Exception as e:
            self.log.error(f"Per-core usage failed: {e}")
            return []

    def get_load_average(self) -> Dict[str, float]:
        try:
            load = psutil.getloadavg()
            return {
                "1min": load[0],
                "5min": load[1],
                "15min": load[2],
            }
        except Exception:
            return {"1min": 0, "5min": 0, "15min": 0}

    def format_for_voice(self) -> str:
        usage = self.get_usage()
        percent = usage.get("percent", 0)
        return f"CPU usage is at {percent} percent, Sir."