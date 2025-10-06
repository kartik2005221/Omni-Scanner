import time
import sys

from omni_scanner.platforms.linux import menu_linux
from omni_scanner.platforms.windows import menu_windows
from omni_scanner.utils.common import clear_screen, splash_screen, oper_system
from omni_scanner.utils.common import install_requirements_once


def main():
    """Main entry point - supports both CLI and interactive modes."""
    try:
        install_requirements_once()
        
        # Check if CLI arguments are provided
        if len(sys.argv) > 1:
            # Try to import and run CLI mode
            try:
                from omni_scanner.ui.cli import app
                app()
                return
            except ImportError:
                print("CLI mode requires additional dependencies. Install with: pip install typer rich")
                print("Falling back to interactive mode...")
                time.sleep(2)
        
        # Interactive mode (original behavior)
        time.sleep(0.7)
        clear_screen()
        splash_screen()
        while True:
            if oper_system == 'windows':
                menu_windows()
            elif oper_system == 'linux':
                menu_linux()
            break
    except KeyboardInterrupt:
        pass
    finally:
        time.sleep(0.5)
        clear_screen()


if __name__ == "__main__":
    main()