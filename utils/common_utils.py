import json
import os
import platform
import subprocess
from datetime import datetime

import utils.documentation_utils as doc_utils

Oper_system = platform.system()
oper_system = Oper_system.lower()


def splash_screen():
    """To print the splash screen"""
    print(r'''
kkkkkkkk                                                          tttt            iiii  kkkkkkkk
k::::::k                                                       ttt:::t           i::::i k::::::k
k::::::k                                                       t:::::t            iiii  k::::::k
k::::::k                                                       t:::::t                  k::::::k
 k:::::k    kkkkkkk  aaaaaaaaaaaaa   rrrrr   rrrrrrrrr   ttttttt:::::ttttttt    iiiiiii  k:::::k    kkkkkkk
 k:::::k   k:::::k   a::::::::::::a  r::::rrr:::::::::r  t:::::::::::::::::t    i:::::i  k:::::k   k:::::k
 k:::::k  k:::::k    aaaaaaaaa:::::a r:::::::::::::::::r t:::::::::::::::::t     i::::i  k:::::k  k:::::k
 k:::::k k:::::k              a::::a rr::::::rrrrr::::::rtttttt:::::::tttttt     i::::i  k:::::k k:::::k
 k::::::k:::::k        aaaaaaa:::::a  r:::::r     r:::::r      t:::::t           i::::i  k::::::k:::::k
 k:::::::::::k       aa::::::::::::a  r:::::r     rrrrrrr      t:::::t           i::::i  k:::::::::::k
 k:::::::::::k      a::::aaaa::::::a  r:::::r                  t:::::t           i::::i  k:::::::::::k
 k::::::k:::::k    a::::a    a:::::a  r:::::r                  t:::::t    tttttt i::::i  k::::::k:::::k
k::::::k k:::::k   a::::a    a:::::a  r:::::r                  t::::::tttt:::::ti::::::ik::::::k k:::::k
k::::::k  k:::::k  a:::::aaaa::::::a  r:::::r                  tt::::::::::::::ti::::::ik::::::k  k:::::k
k::::::k   k:::::k  a::::::::::aa:::a r:::::r                    tt:::::::::::tti::::::ik::::::k   k:::::k
kkkkkkkk    kkkkkkk  aaaaaaaaaa  aaaa rrrrrrr                      ttttttttttt  iiiiiiiikkkkkkkk    kkkkkkk


              ***********************************************************************
              ***********************************************************************
              ****                                                               ****
              ****                © Copyright of Kartik - 2025                   ****
              ****                                                               ****
              ***********************************************************************
              *****************************************************[Ethical Use Only]
                  
## Welcome to Kartik's OmniScanner
''')
    # print(f"## Welcome to Kartik's OmniScanner ({Oper_system} Version)")


def clear_screen():
    """Clearing the screen before running"""
    os.system('cls' if os.name == 'nt' else 'clear')


def documentation(i):
    """To print documentation from documentation_utils.
    :param : 0 for the main menu, 1 for level 1, 2 for level 2, 4 for level 4, p for ports
    :returns : Documentation as string"""

    if i == 0:
        return doc_utils.help0
    elif i == 1:
        return doc_utils.help1
    elif i == 2:
        return doc_utils.help2
    elif i == 3:
        return doc_utils.help3
    elif i == 4:
        return doc_utils.help4
    elif i == 'p':
        return doc_utils.ports
    else:
        return "Documentation not available"


def run_command(command):
    """Running commands, with subprocess
    :param command: Command to run"""
    print("\nExecuting: ", end="")
    for i in command:
        print(i, end=" ")
    print()
    subprocess.run(command)
    input("Press Enter to continue...")

# in testing phase, https://tr.ee/X0qTHG
# def run_command_live(command, scan_type, filename):
#     # Ensure the scans directory exists
#     os.makedirs("scans", exist_ok=True)
#     filepath = os.path.join("scans", filename)
#     process = subprocess.Popen(
#         command,
#         shell=True,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.STDOUT,
#         text=True,
#         bufsize=1
#     )
#     output = ""
#     for line in process.stdout:
#         print(line, end="")
#         output += line
#     process.wait()
#     data = {
#         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "scan_type": scan_type,
#         "result": output
#     }
#     with open(filepath, "w") as f:
#         json.dump(data, f, indent=4)


if __name__ == "__main__":
    # This file is not meant to be run directly
    # It should be imported and used in main.py
    # If this file is run directly, it will print an error message
    print("Wrong file selected for running\nPlease run 'main.py' file by using 'python main.py' command")
