from utils.common_utils import splash_screen, clear_screen, check_sudo, run_with_sudo
from utils.menu_utils import menu

# Actual program starts here
clear_screen()
splash_screen()
if check_sudo() == 0:
    print("Program not running with sudo, Limited functionality available")
    print("Run with sudo for full functionality")
    run_with_sudo()
menu()
input("## Press enter to exit...")
