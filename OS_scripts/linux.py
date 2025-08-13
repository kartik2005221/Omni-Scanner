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
    [1] Arp scan: All IPs on network (less detailed, requires sudo)
    [2] Nmap-Arp scan: Specific IP(s) (less detailed)
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

        elif input2 in ['2']:
            ip_addr = input("\nEnter range of IPs\n" + shell) or "127.0.0.1"
            if validate_ip(ip_addr):
                if input2 == '2':
                    run_command_save(["nmap", "-sn", "-T5", "--min-parallelism", "100", "--host-timeout", "2000ms",
                                      ip_addr], scan)

                # elif input2 == '3':
                #     # try:
                #     #     run_command(["nmap", ip_addr])
                #     # except KeyboardInterrupt:
                #     #     print("\n(Ctrl-C) Exiting...\n\t[Try Fast Scan with option 1,
                #     #     if the user does not have enough time]")
                #     run_command_save(["nmap", ip_addr])
                #     # insert_spinner(["nmap", ip_addr]) # not required for now,,,
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
                        # run_command_save(list_of_commands, scan)

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
    [2] Detect operating system (-o)
    [3] Detect running services and versions (-sV)
    [4] SYN scan (-sS) (stealth scan, requires sudo)
    [5] UDP scan (-sU) (requires sudo)
    [7] Aggressive scan (-A) (slow, detailed)
    [8] Firewall bypass scan (-Pn) (no ping)
    [9] Disable ARP ping (-disable-arp-scan) (router evasion)
   [10] Show all Nmap options (useful for advanced users)
   
Adjustments:
   [p1] Specific ports scan (-p <ports>)
   [p2] Top ports scan (-top-ports <number>)
   [p3] Full ports scan — all ports (-p-)
   
   [a1] Skip DNS lookup (-n)
   [a2] Show only open ports (-open)
   [a3] Adjust Scan Speed and Stealthiness (T0-T5)
    
    [P] Show top 'n' common ports
    [H] Help        [0] Back
            """.rstrip())
        input2 = input(shell).lower() or '0'
        input2 = input2.split()
        time.sleep(0.3)
        if 'h' in input2:
            print(documentation(4))
            input("Enter to go back to menu...")
        elif '0' in input2:
            return 0
        elif 'p' in input2:
            print(documentation('p'))
            input("Enter to go back to menu...")
        elif all(x in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'p1', 'p2', 'p3', 'a1', 'a2', 'a3'] for x in
                 input2):
            ip = input("\nEnter IP to scan\n" + shell) or "127.0.0.1"
            if validate_ip(ip):
                if '1' in input2:
                    run_command_save(["nmap", ip], scan)

                else:
                    list_of_commands = ['nmap']

                    if '2' in input2:
                        list_of_commands.append("-O")

                    if '3' in input2:
                        list_of_commands.append("-sV")

                    if '4' in input2:
                        list_of_commands.append("-sS")

                    if '5' in input2:
                        list_of_commands.append("-sU")

                    if 'p3' in input2:
                        list_of_commands.append("-p-")
                    elif 'p1' in input2:
                        list_of_ports = input("\nEnter port range (Eg. 1-65535) : ") or '1-65535'
                        if validate_port(list_of_ports):
                            list_of_commands.append("-p")
                            list_of_commands.append(list_of_ports)
                    elif 'p2' in input2:
                        number_of_ports = input("\nEnter number of top ports to scan (default 100) : ") or '100'
                        list_of_commands.append("--top-ports")
                        list_of_commands.append(number_of_ports)

                    if '7' in input2:
                        list_of_commands.append("-A")

                    if '8' in input2:
                        list_of_commands.append("-Pn")

                    if '9' in input2:
                        list_of_commands.append("-disable-arp-ping")

                    if '10' in input2:
                        list_of_commands.append("-h")
                        run_command_save(list_of_commands, scan)
                        continue

                    if 'a1' in input2:
                        list_of_commands.append("-n")

                    if 'a2' in input2:
                        list_of_commands.append("--open")

                    if 'a3' in input2:
                        speed = input("\nEnter scan speed (T0-T5, default T3) : ") or 'T3'
                        if speed in ['T0', 'T1', 'T2', 'T3', 'T4', 'T5']:
                            list_of_commands.append(f"-{speed}")
                        elif speed in ['0', '1', '2', '3', '4', '5']:
                            list_of_commands.append(f"-T{speed}")
                        else:
                            print("\nInvalid speed selected, using default T3")
                            list_of_commands.append("-T3")

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