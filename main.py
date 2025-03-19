from utils.administrative_utils import check_and_run_administrative_privilieage
from utils.common_utils import clear_screen, splash_screen
from utils.menu_utils import menu

clear_screen()
splash_screen()
check_and_run_administrative_privilieage()
while True:
    menu()
    if input("Press 0 to exit (finally) :::  ").lower() == '0':
        print("Exiting...")
        clear_screen()
        break
    else:
        print("Aborting Exit...")
