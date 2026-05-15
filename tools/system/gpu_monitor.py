"""
J.A.R.V.I.S. GPU Monitor
Monitors GPU usage and memory.
"""

from typing import Dict, Any

from jarvis_core.logger import Logger


class GPUMonitor:
    def __init__(self):
        self.log = Logger("GPUMonitor")
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("GPU monitor ready.")
        return True

    def get_usage(self) -> Dict[str, Any]:
        try:
            import subprocess

            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu", "--format=csv,noheader,nounits"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == 0 and result.stdout.strip():
                parts = result.stdout.strip().split(",")
                if len(parts) >= 4:
                    return {
                        "utilization_percent": float(parts[0].strip()),
                        "memory_used_mb": float(parts[1].strip()),
                        "memory_total_mb": float(parts[2].strip()),
                        "temperature": float(parts[3].strip()),
                    }

        except FileNotFoundError:
            pass
        except Exception as e:
            self.log.error(f"GPU usage failed: {e}")

        return {
            "utilization_percent": 0,
            "memory_used_mb": 0,
            "memory_total_mb": 0,
            "temperature": 0,
            "available": False,
        }

    def is_available(self) -> bool:
        data = self.get_usage()
        return not data.get("available", False) is False

    def format_for_voice(self) -> str:
        usage = self.get_usage()
        if not usage.get("available", True):
            return "No dedicated GPU detected, Sir."
        return f"GPU at {usage.get('utilization_percent', 0)} percent, {usage.get('memory_used_mb', 0)} megabytes of memory used, Sir."