"""
╔══════════════════════════════════════════════════════════════╗
║                    J.A.R.V.I.S.                              ║
║       Just A Rather Very Intelligent System                  ║
║                                                              ║
║       Entry Point — The Beating Heart                        ║
║       "At your service, Sir."                                ║
╚══════════════════════════════════════════════════════════════╝
"""

import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from jarvis_core.bootloader import Bootloader
from jarvis_core.lifecycle_manager import LifecycleManager
from jarvis_core.crash_handler import CrashHandler
from jarvis_core.config.loader import Config


def main():
    """Bootstrap J.A.R.V.I.S. and run until shutdown."""
    
    # Load configuration
    config = Config.load()
    
    # Wrap everything in crash recovery
    crash_handler = CrashHandler(config)
    
    def run_jarvis():
        """Inner function — the actual boot sequence."""
        bootloader = Bootloader(config)
        
        # Phase 1: Core systems
        bootloader.boot_core()
        
        # Phase 2: Voice pipeline
        bootloader.boot_voice()
        
        # Phase 3: Brain
        bootloader.boot_brain()
        
        # Phase 4: Tools
        bootloader.boot_tools()
        
        # Phase 5: Arc Reactor UI
        bootloader.boot_ui()
        
        # Enter main loop
        lifecycle = LifecycleManager(config)
        lifecycle.run()
    
    crash_handler.execute(run_jarvis)


if __name__ == "__main__":
    main()
