import subprocess
from utils.administrative_utils import check_administrative_privilieage, check_and_run_sudo_linux, is_sudo_linux
from utils.common_utils import documentation
from utils.menu_utils import traceroute_all_os


def level_1():
    """Menu Based : All IP Scanner"""
    while True:
        print("\nSelect a Option:\n\t1. Scan All IPs (High Speed, Less Detailed) (Sudo Required)"
              "\n\t2. Scan specific IPs (Slow speed, More Detailed)\n\tH. Help\n\t0. Previous Menu")
        input2 = input("::: ").lower()
        if input2 == 'h':
            print(documentation(1))
        elif input2 == '0':
            return 0
        elif input2 == '1':
            if check_administrative_privilieage() == 0:
                print("Sudo not detected, Try another option or Switch to SUDO")
            else:
                subprocess.run(["sudo", "arp-scan", "-l"])
        elif input2 == '2':
            try:
                subprocess.run(["nmap", input("Enter range of IPs (eg. 192.168.1.1-100)\n::: ")])
            except KeyboardInterrupt:
                print("\n(Ctrl-C) Exiting...\n\t[Try Fast Scan with option 1, if you dont have enough time]")
        else:
            print("Unsupported Option selected, Please Try again")


def level_2():
    """Menu Based : Ping option's function"""
    while True:
        try:
            print("\nSelect a Option:\n\t1. Simple finite ping\n\t2. Large Ping\n\t3. Ping for slow network"
                  "\n\t4. Flood Ping (requires sudo)(available only in linux/mac)\n\tH. Help\n\t0. Previous Menu")
            input2 = input("::: ").lower()
            if input2 == 'h':
                print(documentation(2))
            elif input2 == '0':
                return 0
            elif input2 == '1':
                subprocess.run(["ping", "-c", "7", input("Enter IP to ping : ")])
            elif input2 == '2':
                subprocess.run(["ping", "-s", input("Enter size of packet to send (0-65500)"),
                                input("Enter IP to ping : ")])
            elif input2 == '3':
                subprocess.run(["ping", "-W", int(input("How much time to wait? ")),
                                input("Enter IP to ping : ")])
            elif input2 == '4':
                if check_administrative_privilieage() == 1:
                    subprocess.run(["sudo", "ping", "-f", input("Enter IP to ping : ")])
                else:
                    print("Sudo not detected, Try another option or Switch to SUDO")
            else:
                print("Unsupported Option selected, Please Try again")
        except KeyboardInterrupt:
            print("Stopping...")
            continue


def level_4():
    """Menu based : All Nmap option's function"""
    while True:
        print("\nSelect Required option: (separated by spaces)"
              "\n\t1. Simple Nmap (Fast)(Dont use it with any other argument)\n\t2. Detect OS\n\t"
              "3. Detect running service & its version"
              "from open ports\n\t4. SYN Scan\n\t5. UDP Scan\n\t6. Specific Port scan \n\t"
              "7. All Port scan(6 or 7, not both)\n\t8. Aggressive Scan (Slower)"
              "\n\tP. Top 50  network ports used.\n\tH. Help\n\t0. Previous Menu")
        input2 = input("::: ").lower()
        if input2 == 'h':
            print(documentation(4))
        elif input2 == '0':
            return 0
        elif input2 == 'p':
            print(documentation('p'))
            input("Enter to go back to previous menu...")
        elif input2 in ['1', '2', '3', '4', '5', '6', '7', '8']:
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
                    list_of_ports = input("Enter port range (Eg. 1-65535) : ") or '1-65535'
                    list_of_commands.append("-p")
                    list_of_commands.append(list_of_ports)

                if '8' in new_input2:
                    list_of_commands.append("-A")

                list_of_commands.append(ip)
                print(list_of_commands)
                subprocess.run(list_of_commands)
        else:
            print("Unsupported Option selected, Please Try again")


def menu_linux():
    """Function for Initial Menu to show in front of user"""
    check_and_run_sudo_linux()
    while True:
        print(r"""
Select a Option :
    1. Scanning full network, Finding Specific Target
    2. Pinging(Custom) a Specific IP
    3. TraceRouting
    4. Advance Scanning a Specific IP
    H. Help
    0. Exit""")
        input1 = input("::: ").lower()

        if input1 == 'h':
            print(documentation(0))
        elif input1 == '0':
            return 0
        elif input1 == '1':
            level_1()
        elif input1 == '2':
            level_2()
        elif input1 == '3':
            traceroute_all_os()
        elif input1 == '4':
            level_4()
        else:
            print("Unsupported Option selected, Please Try again")
