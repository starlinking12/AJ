"""
J.A.R.V.I.S. Daemon Manager
Runs Jarvis as a background daemon process.
"""

import os
import sys
import atexit

from jarvis_core.logger import Logger


class DaemonManager:
    def __init__(self, pidfile: str = "/tmp/jarvis.pid"):
        self.pidfile = pidfile
        self.log = Logger("Daemon")

    def daemonize(self) -> None:
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            self.log.error(f"Fork failed: {e}")
            sys.exit(1)

        os.chdir("/")
        os.setsid()
        os.umask(0)

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            self.log.error(f"Second fork failed: {e}")
            sys.exit(1)

        sys.stdout.flush()
        sys.stderr.flush()

        with open("/dev/null", "r") as f:
            os.dup2(f.fileno(), sys.stdin.fileno())
        with open("/dev/null", "w") as f:
            os.dup2(f.fileno(), sys.stdout.fileno())
            os.dup2(f.fileno(), sys.stderr.fileno())

        atexit.register(self.cleanup)
        self.write_pid()
        self.log.info("Daemonized successfully.")

    def write_pid(self) -> None:
        with open(self.pidfile, "w") as f:
            f.write(str(os.getpid()))

    def cleanup(self) -> None:
        try:
            os.remove(self.pidfile)
        except FileNotFoundError:
            pass