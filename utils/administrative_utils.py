import ctypes
import os
import sys

from utils.common_utils import run_command


# Windows
def is_admin_windows():
    """Check if the script is running with administrative privileges.
    :returns : True if running with admin privilege, else False"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except AttributeError:
        return False


def run_as_admin_windows():
    """to run the current program with admin privilege.
    first take input from the user if he wants to run again with admin privilege or not"""
    if input("Press 0 if you want to exit and run again with sudo\nElse, Press any key...\n: ") == '0':
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",  # "runas" triggers UAC elevation
            sys.executable,
            f'"{sys.argv[0]}"',  # quoted to handle spaces
            None,
            1
        )
        sys.exit()


def check_and_run_admin_windows():
    """Check if not sudo, then Run the script with admin privileges"""
    if not is_admin_windows():
        print("Program not running with administrative privilege, Limited functionality available")
        print("Run with administrative privilege for full functionality")
        run_as_admin_windows()


# Linux
def is_sudo_linux():
    """To check for current program is running with sudo or not.
    :returns : 0 if not running with sudo, else 1"""
    if not 'SUDO_UID' in os.environ.keys():
        return 0
    else:
        return 1


# def run_with_sudo_linux():
#     """To Run current program with sudo.
#     first take input from the user if he wants to run again with sudo or not"""
#     if input("Press 0 if you want to exit and run again with sudo\nElse, Press any key...\n: ") == '0':
#         # run_command(["sudo", "-S", "python3", os.path.basename(__file__)])
#         run_command(["sudo", "python3", os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main.py'))])
#
#     sys.exit()

def run_with_sudo_linux():
    """Ask from the user to run with sudo or not, then Restart the script with sudo privileges."""
    run_command(["sudo", "python3"] + sys.argv)
    sys.exit()


def check_and_run_sudo_linux():
    if not is_sudo_linux():
        print("Program not running with sudo, Limited functionality available")
        print("Run with sudo for full functionality")
        if input("Press 0 if you want to exit and run again with sudo\nElse, Press any key...\n: ") == '0':
            run_with_sudo_linux()


# Common
# def check_administrative_privilieage():
#     """To check for current program is running with administrative access or not,
#     0 -> no administrative access,
#     1 -> administrative access"""
#     if oper_system == 'Windows':
#         is_admin_windows()
#     elif oper_system == 'Linux':
#         is_sudo_linux()
#
# def check_and_run_administrative_privilieage():
#     if oper_system == 'Windows':
#         check_and_run_admin_windows()
#     elif oper_system == 'Linux':
#         check_and_run_sudo_linux()

if __name__ == "__main__":
    # This file is not meant to be run directly
    # It should be imported and used in main.py
    # If this file is run directly, it will print an error message
    print("Wrong file selected for running\nPlease run 'main.py' file by using 'python main.py' command")
