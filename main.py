import time

from OS_scripts.linux import menu_linux
from OS_scripts.windows import menu_windows
from utils.common_utils import clear_screen, splash_screen, oper_system
from utils.module_installer_utils import install_requirements_once

if __name__ == "__main__":
    try:
        # if not is_module_installed("requests"):
        #     print("Installing requests module...")
        #     run_command(["pip", "install", "requests"])
        install_requirements_once()
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
