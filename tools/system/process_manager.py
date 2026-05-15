"""
J.A.R.V.I.S. Process Manager
Manages system processes. Start, stop, list, and monitor.
"""

import subprocess
import platform
from typing import List, Dict, Optional

import psutil

from jarvis_core.logger import Logger


class ProcessManager:
    def __init__(self):
        self.log = Logger("ProcessManager")
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("Process manager ready.")
        return True

    def list_processes(self, limit: int = 20) -> List[Dict]:
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    info = proc.info
                    processes.append({
                        "pid": info['pid'],
                        "name": info['name'] or "unknown",
                        "cpu": info['cpu_percent'] or 0.0,
                        "memory": info['memory_percent'] or 0.0,
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            processes.sort(key=lambda x: x['cpu'], reverse=True)
            return processes[:limit]

        except Exception as e:
            self.log.error(f"Process list failed: {e}")
            return []

    def find_process(self, name: str) -> List[Dict]:
        processes = []
        name_lower = name.lower()
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    if name_lower in (proc.info['name'] or "").lower():
                        processes.append({
                            "pid": proc.info['pid'],
                            "name": proc.info['name'],
                            "cpu": proc.info['cpu_percent'] or 0.0,
                            "memory": proc.info['memory_percent'] or 0.0,
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            self.log.error(f"Process search failed: {e}")

        return processes

    def kill_process(self, pid: int) -> bool:
        try:
            process = psutil.Process(pid)
            process.terminate()
            self.log.info(f"Process terminated: {pid}")
            return True
        except psutil.NoSuchProcess:
            self.log.warn(f"Process not found: {pid}")
            return False
        except Exception as e:
            self.log.error(f"Process kill failed: {e}")
            return False

    def is_running(self, name: str) -> bool:
        name_lower = name.lower()
        try:
            for proc in psutil.process_iter(['name']):
                try:
                    if name_lower in (proc.info['name'] or "").lower():
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception:
            pass
        return False