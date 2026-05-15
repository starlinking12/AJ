"""
J.A.R.V.I.S. Disk Monitor
Monitors disk usage and available space.
"""

from typing import Dict, Any, List

import psutil

from jarvis_core.logger import Logger


class DiskMonitor:
    def __init__(self):
        self.log = Logger("DiskMonitor")
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("Disk monitor ready.")
        return True

    def get_disk_usage(self, path: str = "/") -> Dict[str, Any]:
        try:
            usage = psutil.disk_usage(path)
            return {
                "total_gb": round(usage.total / (1024**3), 2),
                "used_gb": round(usage.used / (1024**3), 2),
                "free_gb": round(usage.free / (1024**3), 2),
                "percent": usage.percent,
            }
        except Exception as e:
            self.log.error(f"Disk usage failed: {e}")
            return {"error": str(e)}

    def get_all_partitions(self) -> List[Dict]:
        partitions = []
        try:
            for part in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(part.mountpoint)
                    partitions.append({
                        "device": part.device,
                        "mountpoint": part.mountpoint,
                        "filesystem": part.fstype,
                        "total_gb": round(usage.total / (1024**3), 2),
                        "used_gb": round(usage.used / (1024**3), 2),
                        "free_gb": round(usage.free / (1024**3), 2),
                        "percent": usage.percent,
                    })
                except PermissionError:
                    continue
        except Exception as e:
            self.log.error(f"Partition list failed: {e}")

        return partitions

    def is_low_on_space(self, path: str = "/", threshold: int = 10) -> bool:
        usage = self.get_disk_usage(path)
        free_gb = usage.get("free_gb", 0)
        return free_gb < threshold