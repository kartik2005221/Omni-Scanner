from OS_scripts.linux import menu_linux
from OS_scripts.windows import menu_windows
from utils.common_utils import clear_screen, splash_screen, oper_system

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
