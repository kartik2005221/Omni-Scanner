import json
import os
import platform
import subprocess
import time
from datetime import datetime

import utils.documentation_utils as doc_utils

Oper_system = platform.system()
oper_system = Oper_system.lower()

shell = "Omni-Scanner > "


# 88                                     88 88        ad88888b,    ,a888a,       ,a888a,    888888888   ad88888b,  ad88888b,     88
# 88                               ,d    "" 88       d8"    "88  ,8P"' `"Y8,   ,8P"' `"Y8,  88         d8"    "88 d8"    "88   ,d88
# 88                               88       88              a8P ,8P       Y8, ,8P       Y8, 88  ___           a8P        a8P 888888
# 88   ,d8 ,adPPYYba, 8b,dPPYba, MM88MMM 88 88   ,d8      ,8P"  88         88 88         88 88a8PPP8b,      ,8P"       ,8P"      88
# 88 ,a8"  ""     `Y8 88P'   "Y8   88    88 88 ,a8"     a8P     88         88 88         88 PP"    `8b    a8P        a8P         88
# 8888[    ,adPPPPP88 88           88    88 8888[     a8P'      `8b       d8' `8b       d8'         d8  a8P'       a8P'          88
# 88`"Yba, 88,    ,88 88           88,   88 88`"Yba, d8"         `8ba, ,ad8'   `8ba, ,ad8'  Y8a    a8P d8"        d8"            88
# 88   `Y8 `"8bbdP"Y8 88           "Y888 88 88   `Y8a8888888888    "Y888P"       "Y888P"     "Y8888P"  8888888888 8888888888     88

# kkkkkkkk                                                          tttt            iiii  kkkkkkkk
# k::::::k                                                       ttt:::t           i::::i k::::::k
# k::::::k                                                       t:::::t            iiii  k::::::k
# k::::::k                                                       t:::::t                  k::::::k
#  k:::::k    kkkkkkk  aaaaaaaaaaaaa   rrrrr   rrrrrrrrr   ttttttt:::::ttttttt    iiiiiii  k:::::k    kkkkkkk
#  k:::::k   k:::::k   a::::::::::::a  r::::rrr:::::::::r  t:::::::::::::::::t    i:::::i  k:::::k   k:::::k
#  k:::::k  k:::::k    aaaaaaaaa:::::a r:::::::::::::::::r t:::::::::::::::::t     i::::i  k:::::k  k:::::k
#  k:::::k k:::::k              a::::a rr::::::rrrrr::::::rtttttt:::::::tttttt     i::::i  k:::::k k:::::k
#  k::::::k:::::k        aaaaaaa:::::a  r:::::r     r:::::r      t:::::t           i::::i  k::::::k:::::k
#  k:::::::::::k       aa::::::::::::a  r:::::r     rrrrrrr      t:::::t           i::::i  k:::::::::::k
#  k:::::::::::k      a::::aaaa::::::a  r:::::r                  t:::::t           i::::i  k:::::::::::k
#  k::::::k:::::k    a::::a    a:::::a  r:::::r                  t:::::t    tttttt i::::i  k::::::k:::::k
# k::::::k k:::::k   a::::a    a:::::a  r:::::r                  t::::::tttt:::::ti::::::ik::::::k k:::::k
# k::::::k  k:::::k  a:::::aaaa::::::a  r:::::r                  tt::::::::::::::ti::::::ik::::::k  k:::::k
# k::::::k   k:::::k  a::::::::::aa:::a r:::::r                    tt:::::::::::tti::::::ik::::::k   k:::::k
# kkkkkkkk    kkkkkkk  aaaaaaaaaa  aaaa rrrrrrr                      ttttttttttt  iiiiiiiikkkkkkkk    kkkkkkk
#               ***********************************************************************
#               ***********************************************************************
#               ****                                                               ****
#               ****            © Copyright of @kartik2005221 - 2025               ****
#               ****                                                               ****
#               ***********************************************************************
#               *****************************************************[Ethical Use Only]


def splash_screen():
    """To print the splash screen"""
    print(r'''╔═══════════════════════════════════════════════════════╗
║                                                       ║
║   ░█▀█░█▄█░█▀█░▀█▀░░░░░█▀▀░█▀▀░█▀█░█▀█░█▀█░█▀▀░█▀▄    ║
║   ░█░█░█░█░█░█░░█░░▄▄▄░▀▀█░█░░░█▀█░█░█░█░█░█▀▀░█▀▄    ║
║   ░▀▀▀░▀░▀░▀░▀░▀▀▀░░░░░▀▀▀░▀▀▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀░▀    ║
║                                                       ║
║                 Omni-Scanner v1.0                     ║
║                Crafted by AiR ©2025                   ║
║        An All-in-One Network Scanning Tool            ║
║                                                       ║
╚═════════════════════════════════════[Ethical Use Only]╝
## Welcome to Omni-Scanner''')
    time.sleep(1)
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


# def run_command(command):
#     """Running commands, with subprocess
#     :param command: Command to run"""
#     print("\nExecuting: ", end="")
#     for i in command:
#         print(i, end=" ")
#     print()
#     subprocess.run(command)
#     input("Press Enter to continue...")


process = None
output = None


def run_command_save(command, scan_type="other-scan"):
    global process, output

    print("\nExecuting: ", end="")
    for i in command:
        print(i, end=" ")
    print()
    filename = f"{scan_type}.json"  # Ensure the scans directory exists
    os.makedirs("scans", exist_ok=True)
    filepath = os.path.join("scans", filename)
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        # output = ""
        output = []
        for line in process.stdout:
            print(line, end="")
            # output += line
            output.append(line.strip())  # Store each line of output
        process.wait()
    except KeyboardInterrupt:
        process.terminate()
        print("\nProcess terminated by user.")
    else:
        input("Press Enter to continue...")
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "scan_type": scan_type,
        "operating_system": Oper_system,
        "command": " ".join(command),
        "result": output,
    }
    if os.path.exists(filepath):  # Read existing data or make an empty list
        with open(filepath, "r") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []
    existing_data.append(data)
    with open(filepath, "w") as f:  # Write updated data back to the file
        json.dump(existing_data, f, indent=4)

    time.sleep(0.3)


# run_command_live("echo 'Running scan...1'", "test1_scan")

if __name__ == "__main__":
    # This file is not meant to be run directly
    # It should be imported and used in main.py
    # If this file is run directly, it will print an error message
    print("Wrong file selected for running\nPlease run 'main.py' file by using 'python main.py' command")