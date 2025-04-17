from OS_scripts.linux import menu_linux
from OS_scripts.windows import menu_windows
from utils.common_utils import clear_screen, splash_screen, oper_system
from utils.installer_utils import install_requirements_once

if __name__ == "__main__":
    try:
        # if not is_module_installed("requests"):
        #     print("Installing requests module...")
        #     run_command(["pip", "install", "requests"])
        install_requirements_once()
        clear_screen()
        splash_screen()
        while True:
            if oper_system == 'windows':
                menu_windows()
            elif oper_system == 'linux':
                menu_linux()

            exit_finally = input("Press 0 to exit (finally) :::  ") or '1'
            if exit_finally.lower() == '0':
                print("Exiting...")
                clear_screen()
                break
            else:
                print("Aborting Exit...")
    except KeyboardInterrupt:
        try:
            input("\n[Ctrl-C] Exiting...")
        except KeyboardInterrupt:
            pass
        finally:
            clear_screen()
            exit(0)
