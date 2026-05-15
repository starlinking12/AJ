"""
J.A.R.V.I.S. Network Monitor
Monitors network connections and bandwidth usage.
"""

from typing import Dict, Any, List

import psutil

from jarvis_core.logger import Logger


class NetworkMonitor:
    def __init__(self):
        self.log = Logger("NetworkMonitor")
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("Network monitor ready.")
        return True

    def get_network_stats(self) -> Dict[str, Any]:
        try:
            net_io = psutil.net_io_counters()
            return {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv,
                "mb_sent": round(net_io.bytes_sent / (1024**2), 2),
                "mb_recv": round(net_io.bytes_recv / (1024**2), 2),
            }
        except Exception as e:
            self.log.error(f"Network stats failed: {e}")
            return {"error": str(e)}

    def get_connections(self) -> List[Dict]:
        connections = []
        try:
            for conn in psutil.net_connections(kind='inet'):
                connections.append({
                    "local_address": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "",
                    "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "",
                    "status": conn.status,
                    "pid": conn.pid,
                })
        except Exception as e:
            self.log.error(f"Connections list failed: {e}")

        return connections[:20]

    def is_online(self) -> bool:
        try:
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except Exception:
            return False

    def get_interface_info(self) -> List[Dict]:
        interfaces = []
        try:
            for name, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == 2:
                        interfaces.append({
                            "name": name,
                            "ip": addr.address,
                            "netmask": addr.netmask,
                        })
        except Exception as e:
            self.log.error(f"Interface info failed: {e}")

        return interfaces