"""
J.A.R.V.I.S. Timezone Lookup
Provides timezone information for cities.
"""

from typing import Optional
from datetime import datetime
import time

from jarvis_core.logger import Logger


class TimezoneLookup:
    def __init__(self):
        self.log = Logger("TimezoneLookup")
        self._timezone_offsets = {
            "America/New_York": "UTC-5",
            "America/Chicago": "UTC-6",
            "America/Denver": "UTC-7",
            "America/Los_Angeles": "UTC-8",
            "Europe/London": "UTC+0",
            "Europe/Paris": "UTC+1",
            "Europe/Berlin": "UTC+1",
            "Europe/Moscow": "UTC+3",
            "Asia/Dubai": "UTC+4",
            "Asia/Kolkata": "UTC+5:30",
            "Asia/Shanghai": "UTC+8",
            "Asia/Tokyo": "UTC+9",
            "Australia/Sydney": "UTC+10",
            "Pacific/Auckland": "UTC+12",
        }

    def get_offset(self, timezone: str) -> Optional[str]:
        if timezone in self._timezone_offsets:
            return self._timezone_offsets[timezone]
        return None

    def get_current_time(self, timezone: str) -> Optional[str]:
        try:
            import zoneinfo
            tz = zoneinfo.ZoneInfo(timezone)
            current = datetime.now(tz)
            return current.strftime("%H:%M, %A, %d %B %Y")
        except ImportError:
            return None
        except Exception as e:
            self.log.error(f"Timezone error: {e}")
            return None

    def compare_timezones(self, tz1: str, tz2: str) -> str:
        try:
            import zoneinfo
            from datetime import datetime

            time1 = datetime.now(zoneinfo.ZoneInfo(tz1))
            time2 = datetime.now(zoneinfo.ZoneInfo(tz2))

            diff = time1.hour - time2.hour

            if diff > 0:
                return f"{tz1} is {diff} hours ahead of {tz2}"
            elif diff < 0:
                return f"{tz1} is {abs(diff)} hours behind {tz2}"
            else:
                return f"{tz1} and {tz2} are in the same time zone"
        except Exception:
            return "Unable to compare timezones."

    def list_common_timezones(self) -> list:
        return list(self._timezone_offsets.keys())