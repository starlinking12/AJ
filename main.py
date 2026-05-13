import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from jarvis_core.bootloader import Bootloader
from jarvis_core.lifecycle_manager import LifecycleManager
from jarvis_core.crash_handler import CrashHandler
from jarvis_core.config.loader import Config


def main():
    config = Config.load()
    crash_handler = CrashHandler(config)
    
    def run_jarvis():
        bootloader = Bootloader(config)
        bootloader.boot_core()
        bootloader.boot_voice()
        bootloader.boot_brain()
        bootloader.boot_tools()
        bootloader.boot_ui()
        
        lifecycle = LifecycleManager(config)
        lifecycle.run()
    
    crash_handler.execute(run_jarvis)


if __name__ == "__main__":
    main()