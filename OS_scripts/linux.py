import time

from utils.administrative_utils import check_and_run_sudo_linux, is_sudo_linux, run_with_sudo_linux
from utils.common_utils import documentation, run_command_save, shell
from utils.menu_utils import validate_ip_addr, insert_spinner, get_mac_vendor, \
    validate_mac, run_nmap_scan_firewall, validate_port, validate_ip


def level_1():
    """Menu Based : All IP Scanner"""
    scan = "arp-scan"
    while True:
        print(r"""
Select an Option:
    [1] Fast scan: All IPs on network (less detailed, requires sudo)
    [2] Fast scan: Specific IP(s) (less detailed)
    [3] Deep scan: Specific IP(s) (more detailed, slower)
    [H] Help        [0] Back
            """.rstrip())
        input2 = input(shell).lower() or '0'
        time.sleep(0.3)
        if input2 == 'h':
            print(documentation(1))
            input("Enter to go back to menu...")
        elif input2 == '0':
            return 0
        elif input2 == '1':
            if not is_sudo_linux():
                print("\nSudo not detected, \nTry another option or Switch to SUDO (Option 5 in previous menu)")
            else:
                run_command_save(["sudo", "arp-scan", "-l"], scan)

        elif input2 in ['2', '3']:
            ip_addr = input("\nEnter range of IPs (eg. 192.168.1.1-255)\n" + shell) or "127.0.0.1"
            if validate_ip(ip_addr):
                if input2 == '2':
                    run_command_save(["nmap", "-sn", "-T5", "--min-parallelism", "100", "--host-timeout", "2000ms",
                                      ip_addr], scan)

                elif input2 == '3':
                    # try:
                    #     run_command(["nmap", ip_addr])
                    # except KeyboardInterrupt:
                    #     print("\n(Ctrl-C) Exiting...\n\t[Try Fast Scan with option 1,
                    #     if the user does not have enough time]")
                    run_command_save(["nmap", ip_addr])
                    # insert_spinner(["nmap", ip_addr]) # not required for now,,,
            else:
                print("\nInvalid IP Address, please try again")
        # elif input2 == '4':
        #     mac_addr = input("Enter MAC Address to look up
        #     (e.g., 00:00:00:00:00:00)\nOmni-Scanner > ") or "00:00:00:00:00:00"
        #     if validate_mac(mac_addr):
        #         print(f"Mac Vendor for {mac_addr} is {get_mac_vendor(mac_addr)}")
        #     else:
        #         print ("Invalid MAC Address entered, Please Try again")
        #     # print(get_mac_vendor(mac_addr))
        else:
            print("\nUnsupported Option selected, Please Try again")
        time.sleep(0.3)


def _append_to_list_ping(input2, list_of_commands, flood=False):
    if '2' in input2:
        list_of_commands.append('-s')
        list_of_commands.append(input("\nEnter size of packet to send (0-65500)\n" + shell) or '56')
    if '3' in input2:
        list_of_commands.append('-W')
        list_of_commands.append(input("\nHow much time(sec.) to wait? \n" + shell) or '1')
    if flood:
        if is_sudo_linux() == 1:
            list_of_commands.insert(0, "sudo")
            list_of_commands.append("-f")
        else:
            print("\nSudo not detected, Try another option or Switch to SUDO")


def _finite_or_infinite_ping(list_of_commands):
    """To run ping command with infinite or finite options"""
    ping_type = input("\nPing finitely or infinitely? (1/2)\n" + shell) or '1'
    if ping_type == '1':
        no_of_packets = input("\nEnter number of packets to send\n" + shell) or '5'
        list_of_commands.append("-c")
        list_of_commands.append(no_of_packets)
    elif ping_type == '2':
        pass


def level_2():
    """Menu Based : Ping option's function"""
    scan = "ping-scan"
    while True:
        try:
            print(r"""
Select required options (separate by space):
    [1] Simple ping — use alone, not with other options
    [2] Bigger packet size of ping
    [3] Slow-network ping
    [4] Flood ping (sudo required)
    [H] Help        [0] Back
            """.rstrip())
            input2 = input(shell).lower() or '0'
            time.sleep(0.3)
            if input2 == 'h':
                print(documentation(2))
                input("Enter to go back to menu...")
            elif input2 == '0':
                return 0
            elif all(x in ['1', '2', '3', '4'] for x in input2):
                ip_addr = input("\nEnter IP to ping\n" + shell) or "127.0.0.1"
                if validate_ip_addr(ip_addr):
                    list_of_commands = ['ping']
                    if input2 == '1':
                        list_of_commands.append(ip_addr)
                        run_command_save(list_of_commands, scan)

                    flood = '4' in input2
                    _append_to_list_ping(input2, list_of_commands, flood=flood)

                    if not flood:
                        _finite_or_infinite_ping(list_of_commands)

                    list_of_commands.append(ip_addr)
                    run_command_save(list_of_commands, scan)

                    # clear but longer same logic for-above-code
                    # if '4' not in input2:
                    #     _append_to_list_ping(input2, list_of_commands)
                    #     _finite_or_infinite_ping(list_of_commands)
                    #     list_of_commands.append(ip_addr)
                    #     run_command_save(list_of_commands, scan)
                    # elif '4' in input2:
                    #     _append_to_list_ping(input2, list_of_commands, flood=True)
                    #     list_of_commands.append(ip_addr)
                    #     run_command_save(list_of_commands, scan)

                else:
                    print("\nInvalid IP entered, Please Try again")
            else:
                print("\nUnsupported Option selected, Please Try again")
        except KeyboardInterrupt:
            print("Stopping...")
            continue
        finally:
            time.sleep(0.3)


def level_3():
    """Menu Based : Traceroute option's function"""
    scan = "traceroute-scan"
    while True:
        print(r"""
Select an Option:
    [1] Standard Traceroute (ICMP/UDP)
    [2] Firewall-Evasion Traceroute (TCP port 80) (sudo required)
    [H] Help        [0] Back
            """.rstrip())
        input2 = input(shell).lower() or '0'
        time.sleep(0.3)
        if input2 == 'h':
            print(documentation(3))
            input("Enter to go back to menu...")
        elif input2 == '0':
            return 0
        elif input2 in ['1', '2']:
            ip_addr = input("\nEnter IP for traceroute : ") or "127.0.0.1"
            # if validate_ip(ip_addr):
            if input2 == '1':
                run_command_save(["traceroute", ip_addr], scan)
            elif input2 == '2':
                if is_sudo_linux() == 1:
                    run_command_save(["sudo", "traceroute", "-T", "-O", "info", "-p", "80", ip_addr], scan)
                else:
                    print("\nSudo not detected, Try another option or Switch to SUDO")
            # else:
            #     print ("Invalid IP entered, Please Try again")
        else:
            print("\nUnsupported Option selected, Please Try again")
        time.sleep(0.3)


def level_4():
    """Menu based : All Nmap option's function"""
    scan = "nmap-scan"
    while True:
        print(r"""
Select required options (separate by space):
    [1] Simple Nmap scan (fast) — use alone, not with other options
    [2] Detect operating system
    [3] Detect running services and versions
    [4] SYN scan
    [5] UDP scan
    [6] Specific port scan
    [7] Full port scan — all 65535 ports (use *either* 6 or 7, not both)
    [8] Aggressive scan (slow, detailed)
    [9] Firewall bypass scan
   [10] Disable ARP ping (router evasion)
    [P] Show top 50 common ports
    [H] Help        [0] Back
            """.rstrip())
        input2 = input(shell).lower() or '0'
        input2 = input2.split()
        time.sleep(0.3)
        if input2 == 'h':
            print(documentation(4))
            input("Enter to go back to menu...")
        elif '0' in input2:
            return 0
        elif 'p' in input2:
            print(documentation('p'))
            input("Enter to go back to menu...")
        # elif input2 in ['1', '2', '3', '4', '5', '6', '7', '8']:
        elif all(x in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] for x in input2):
            ip = input("\nEnter IP to scan\n" + shell) or "127.0.0.1"
            if validate_ip(ip):
                if input2 == '1':
                    run_command_save(["nmap", ip], scan)

                else:
                    # print(new_input23)
                    list_of_commands = ['nmap']

                    if '2' in input2:
                        list_of_commands.append("-O")

                    if '3' in input2:
                        list_of_commands.append("-sV")

                    if '4' in input2:
                        list_of_commands.append("-sS")

                    if '5' in input2:
                        list_of_commands.append("-sU")

                    if '7' in input2:
                        list_of_commands.append("-p-")
                    elif '6' in input2:
                        list_of_ports = input("\nEnter port range (Eg. 1-65535) : ") or '1-65535'
                        if validate_port(list_of_ports):
                            list_of_commands.append("-p")
                            list_of_commands.append(list_of_ports)

                    if '8' in input2:
                        list_of_commands.append("-A")

                    if '9' in input2:
                        list_of_commands.append("-Pn")

                    if '10' in input2:
                        list_of_commands.append("-disable-arp-ping")

                    list_of_commands.append(ip)
                    # print(list_of_commands)
                    # run_command(list_of_commands)
                    run_nmap_scan_firewall(list_of_commands)
            else:
                print("\nInvalid IP entered, Please Try again")
        else:
            print("\nUnsupported Option selected, Please Try again")
        time.sleep(0.3)


def menu_linux():
    """Function for Initial Menu to show in front of the user"""
    check_and_run_sudo_linux()
    print(f"(Linux {'Full' if is_sudo_linux() else 'Limited'} Functionality Version)")
    while True:
        print(r"""
Select an Option:
    [1] Scan full network (find specific host)
    [2] Ping custom IP
    [3] Trace routing
    [4] Advanced scan (may require sudo)
    [5] MAC vendor lookup (online)
    [6] Show network info""" +
              ("" if is_sudo_linux() else "\n    [S] Switch to SUDO") +
              r"""
    [H] Help        [0] Quit
              """.rstrip())
        input1 = input(shell).lower() or '0'
        time.sleep(0.3)

        if input1 == 'h':
            print(documentation(0))
            input("Enter to go back to menu...")
        elif input1 == '0':
            return 0
        elif input1 == '1':
            level_1()
        elif input1 == '2':
            level_2()
        elif input1 == '3':
            level_3()
        elif input1 == '4':
            level_4()
        elif input1 == '5':
            mac_addr = input(
                "\nEnter MAC Address to look up (eg. 00:00:00:00:00:00)\n" + shell) or "00:00:00:00:00:00"
            if validate_mac(mac_addr):
                print(f"\nMac Vendor is {get_mac_vendor(mac_addr)}")
            else:
                print("\nInvalid MAC Address entered, Please Try again")
        elif input1 == '6':
            run_command_save(["ip", "a"])
        elif input1 == 's':
            if not is_sudo_linux():
                print("\nSwitching to SUDO...")
                run_with_sudo_linux()
            else:
                print("Already running with sudo")
        else:
            print("\nUnsupported Option selected, Please Try again")
        time.sleep(0.3)


if __name__ == "__main__":
    # This file is not meant to be run directly
    # It should be imported and used in main.py
    # If this file is run directly, it will print an error message
    print("Wrong file selected for running\nPlease run 'main.py' file by using 'python main.py' command")