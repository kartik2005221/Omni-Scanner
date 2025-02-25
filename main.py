# importing all required modules here
import subprocess
import re
import csv
import os
import time
import shutil
from datetime import datetime
import platform
import documentation

oper_system = platform.system()


# declaring all required functions here
def clear_screen():
    """Clearing the screen before running"""
    os.system('cls' if os.name == 'nt' else 'clear')


def splash_screen():
    """To print splash screen"""
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

## Welcome to Kartik's OmniScanner''')


def check_sudo():
    """To check for current program is running with sudo or not,
    0 -> no sudo,
    1 -> sudo"""
    if not 'SUDO_UID' in os.environ.keys():
        return 0
    else:
        return 1


def run_with_sudo():
    """To Run again program with sudo.
    first take input from user, if he wants to run again with sudo or not"""
    if input("Press 0 if you want to exit and run again with sudo\nElse, Press any key...\n: ") == '0':
        if oper_system.lower() == 'linux':
            subprocess.run(["sudo", "-S", "python", os.path.basename(__file__)])
        elif oper_system.lower() == 'windows':
            subprocess.run(["sudo", "python", os.path.basename(__file__)])
        exit()


def level_1():
    """Menu Based : All IP Scanner"""
    print("\nSelect a Option:\n\t1. Scan All IPs (High Speed, Less Detailed) (Sudo Required)"
          "\n\t2. Scan specific IPs (Slow speed, More Detailed)\n\tH. Help\n\t0. Previous Menu")
    input2 = input("::: ").lower()
    if input2 == 'h':
        print(documentation.help1)
    elif input2 == '0':
        return 0
    elif input2 == '1':
        if check_sudo() == 0:
            print("Sudo not detected, Try another option or Switch to SUDO")
        else:
            subprocess.run(["sudo", "arp-scan", "-l"])
    elif input2 == '2':
        # print("entered")
        subprocess.run(["nmap", input("Enter range of IPs (eg. 192.168.1.1-100)\n::: ")])
    else:
        print("Unsupported Option selected, Please Try again")
    level_1()


def level_2():
    """Menu Based : Ping option's function"""
    while True:
        try:
            print("\nSelect a Option:\n\t1. Simple finite ping\n\t2. Large Ping\n\t3. Ping for slow network"
                  "\n\t4. Flood Ping (requires sudo)(available only in linux/mac)\n\tH. Help\n\t0. Previous Menu")
            input2 = input("::: ").lower()
            if input2 == 'h':
                print(documentation.help2)
            elif input2 == '0':
                return 0
            elif input2 == '1':
                if oper_system.lower() == 'windows':
                    argu = "-n"
                else:
                    argu = "-c"
                subprocess.run(["ping", argu, "7", input("Enter IP to ping : ")])
            elif input2 == '2':
                if oper_system.lower() == 'windows':
                    argu = "-l"
                else:
                    argu = "-s"
                subprocess.run(["ping", argu, "65507", input("Enter IP to ping : ")])
            elif input2 == '3':
                if oper_system.lower() == 'windows':
                    argu = "-w"
                    multiplier = 1000
                else:
                    argu = "-W"
                    multiplier = 1
                subprocess.run(["ping", argu, int(input("How much time to wait? ")) * multiplier,
                                input("Enter IP to ping : ")])
            elif input2 == '4':
                if oper_system.lower() == 'linux':
                    if check_sudo() == 1:
                        subprocess.run(["sudo", "ping", "-f", input("Enter IP to ping : ")])
                    else:
                        print("Sudo not detected, Try another option or Switch to SUDO")
                else:
                    print("Sorry, Flood ping not possible in your operating system")
            else:
                print("Unsupported Option selected, Please Try again")
        except KeyboardInterrupt:
            print("Stopping...")
        level_2()

def level_3():
    """Just a Simple Traceroute Function"""
    subprocess.run(["traceroute", input("Enter IP for traceroute : ")])
    return 0


def level_4():
    """Menu based : All Nmap option's function"""
    print("\nSelect Required option: (separated by spaces)"
          "\n\t1. Simple Nmap (Fast)(Dont use it with any other argument)\n\t2. Detect OS\n\t"
          "3. Detect running service & its version"
          "from open ports\n\t4. SYN Scan\n\t5. UDP Scan\n\t6. Specific Port scan \n\t"
          "7. All Port scan(6 or 7, not both)\n\t8. Aggressive Scan (Slower)"
          "\n\tP. Top 50  network ports used.\n\tH. Help\n\t0. Previous Menu")
    input2 = input("::: ").lower()
    if input2 == 'h':
        print(documentation.help4)
    elif input2 == '0':
        return 0
    elif input2 == 'p':
        print(documentation.ports)
    else:
        ip = input("Enter IP to scan : ")
        if input2 == '1':
            subprocess.run(["nmap", ip])
        else:
            new_input2 = input2.split()
            # print(new_input2)
            list_of_commands = ['nmap']

            if '2' in new_input2:
                list_of_commands.append("-O")

            if '3' in new_input2:
                list_of_commands.append("-sV")

            if '4' in new_input2:
                list_of_commands.append("-sS")

            if '5' in new_input2:
                list_of_commands.append("-sU")

            if '7' in new_input2:
                list_of_commands.append("-p-")
            elif '6' in new_input2:
                list_of_ports = input("Enter port range (Eg. 1-65535) : ")
                list_of_commands.append("-p")
                list_of_commands.append(list_of_ports)

            if '8' in new_input2:
                list_of_commands.append("-A")

            list_of_commands.append(ip)
            print(list_of_commands)
            subprocess.run(list_of_commands)
    level_4()


def menu():
    """Function for Initial Menu to show in front of user"""
    while True:
        print(r"""
Select a Option :
    1. Scanning full network, Finding Specific Target
    2. Pinging(Custom) a Specific IP
    3. TraceRouting
    4. Advance Scanning a Specific IP
    H. Help
    X. Exit""")
        input1 = input("::: ").lower()

        if input1 == 'h':
            print(documentation.help0)
        elif input1 == 'x':
            break
        elif input1 == '1':
            level_1()
        elif input1 == '2':
            level_2()
        elif input1 == '3':
            level_3()
        elif input1 == '4':
            level_4()
        else:
            print("Unsupported Option selected, Please Try again")

    # sample codes for reference
    # result = subprocess.run(["arp-scan", "-l"], capture_output=True, text=True)
    # print("Output:", result.stdout)
    # print("Error:", result.stderr)
    # print("Return Code:", result.returncode)


# Actual program starts here
clear_screen()
splash_screen()
if check_sudo() == 0:
    print("Program not running with sudo, Limited functionality available")
    print("Run with sudo for full functionality")
    run_with_sudo()
menu()
input("## Press enter to exit...")
