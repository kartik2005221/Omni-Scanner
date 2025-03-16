import subprocess
from utils import documentation_utils
from utils.common_utils import check_sudo, oper_system


def level_1():
    """Menu Based : All IP Scanner"""
    print("\nSelect a Option:\n\t1. Scan All IPs (High Speed, Less Detailed) (Sudo Required)"
          "\n\t2. Scan specific IPs (Slow speed, More Detailed)\n\tH. Help\n\t0. Previous Menu")
    input2 = input("::: ").lower()
    if input2 == 'h':
        print(documentation_utils.help1)
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
                print(documentation_utils.help2)
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
        print(documentation_utils.help4)
    elif input2 == '0':
        return 0
    elif input2 == 'p':
        print(documentation_utils.ports)
        input("Enter to go back to previous menu...")
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
            print(documentation_utils.help0)
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
