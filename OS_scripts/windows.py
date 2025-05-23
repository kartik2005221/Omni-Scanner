import time

from utils.common_utils import documentation, run_command_save
from utils.menu_utils import validate_ip, validate_ip_range, insert_spinner, get_mac_vendor, validate_mac, \
    run_tcp_traceroute_windows, run_nmap_scan_firewall, validate_port


def level_1():
    """Menu Based : All IP Scanner"""
    scan = "arp-scan"
    while True:
        print(r"""
Select an Option:
    [1] Fast scan: All IPs on network (less detailed, *linux only)
    [2] Fast scan: Specific IP(s) (less detailed)
    [3] Deep scan: Specific IP(s) (more detailed, slower)
    [H] Help        [0] Back
            """.rstrip())
        input2 = input("Omni-Scanner > ").lower() or '0'
        time.sleep(0.3)
        if input2 == 'h':
            print(documentation(1))
            input("Enter to go back to menu...")
        elif input2 == '0':
            return 0
        elif input2 == '1':
            print("\nSorry, This option is not available in your operating system")
        elif input2 in ['2', '3']:
            ip_addr = input("\nEnter range of IPs (eg. 192.168.1.1-255)\nOmni-Scanner > ") or "127.0.0.1"
            if validate_ip_range(ip_addr):
                if input2 == '2':
                    run_command_save(["nmap", "-sn", "-T5", "--min-parallelism", "100",
                                      "--host-timeout", "2000ms", ip_addr], scan)

                elif input2 == '3':
                    # try:
                    #     subprocess.run(["nmap", ip_addr])
                    # except KeyboardInterrupt:
                    #     print("\n(Ctrl-C) Exiting...\n\t[Try Fast Scan with option 1,
                    #     if the user does not have enough time]")
                    insert_spinner(["nmap", ip_addr])
            else:
                print("\nInvalid IP range entered, Please Try again")
        # elif input2 == '4':
        #     mac_addr = input("Enter MAC Address to look up
        #     (e.g., 00:00:00:00:00:00)\nOmni-Scanner > ") or "00:00:00:00:00:00"
        #     if validate_mac(mac_addr):
        #         print(f"Mac Vendor for {mac_addr} is {get_mac_vendor(mac_addr)}")
        #     else:
        #         print ("Invalid MAC Address entered, Please Try again")
        else:
            print("\nUnsupported Option selected, Please Try again")
        time.sleep(0.3)


def level_2():
    """Menu Based : Ping option's function"""
    scan = "ping-scan"
    while True:
        try:
            print(r"""
Select an Option:
    [1] Simple ping
    [2] Extended ping
    [3] Slow-network ping
    [4] Flood ping (linux only)
    [H] Help        [0] Back
            """.rstrip())
            input2 = input("Omni-Scanner > ").lower() or '0'
            time.sleep(0.3)
            if input2 == 'h':
                print(documentation(2))
                input("Enter to go back to menu...")
            elif input2 == '0':
                return 0
            elif input2 in ['1', '2', '3']:
                ip_addr = input("\nEnter IP to ping (eg 192.168.1.1)\nOmni-Scanner > ") or "127.0.0.1"
                if validate_ip(ip_addr):
                    ping_type = input("\nPing finitely or infinitely? (1/2)\nOmni-Scanner > ") or '1'
                    if ping_type == '1':
                        no_of_packets = input("\nEnter number of packets to send\nOmni-Scanner > ") or '5'
                        ping_count = f"-n {no_of_packets}"
                    else:
                        ping_count = "-t"

                    if input2 == '1':
                        run_command_save(["ping", ping_count, ip_addr], scan)

                    elif input2 == '2':
                        run_command_save(
                            ["ping", ping_count, "-l", input("\nEnter size of packet to send (0-65500)"), ip_addr],
                            scan)

                    elif input2 == '3':
                        run_command_save(
                            ["ping", ping_count, "-w",
                             str(int(input("\nHow much time (sec.) to wait?\nOmni-Scanner > ")) * 1000),
                             ip_addr], scan)

                else:
                    print("\nInvalid IP entered, Please Try again")
            elif input2 == '4':
                print("\nSorry, Flood ping not possible in your operating system")
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
    [2] Firewall-Evasion Traceroute (TCP port 80) (linux only)
    [H] Help        [0] Back
            """.rstrip())
        input2 = input("Omni-Scanner > ").lower() or '0'
        time.sleep(0.3)
        if input2 == 'h':
            print(documentation(3))
            input("Enter to go back to menu...")
        elif input2 == '0':
            return 0
        elif input2 in ['1', '2']:
            ip_addr = input("\nEnter IP/Domain for traceroute : ") or "127.0.0.1"
            # if validate_ip(ip_addr):
            if input2 == '1':
                run_command_save(["tracert", ip_addr], scan)
            elif input2 == '2':
                # run_command_save(["nmap", "--traceroute", "-p", "80", ip_addr])
                run_tcp_traceroute_windows(ip_addr)
            # else:
            #     print ("Invalid IP entered, Please Try again")
        else:
            print("\nUnsupported Option selected, Please Try again")
        time.sleep(0.3)


def level_4(number_of_ip=0):
    """Menu based : All Nmap option's function"""
    if number_of_ip == 0:
        validate = validate_ip
    else:
        validate = validate_ip_range

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
        input2 = input("Omni-Scanner > ").lower() or '0'
        time.sleep(0.3)
        input2 = input2.split()

        if 'h' in input2:
            print(documentation(4))
            input("Enter to go back to menu...")
        elif '0' in input2:
            return 0
        elif 'p' in input2:
            print(documentation('p'))
            input("Enter to go back to menu...")
        # elif input2 in ['1', '2', '3', '4', '5', '6', '7', '8']:
        elif all(x in ['1', '2', '3', '4', '5', '6', '7', '8'] for x in input2):
            ip_addr = input("\nEnter IP to scan(eg - 192.168.1.1)\nOmni-Scanner > ") or "127.0.0.1"
            if validate(ip_addr):
                if '1' in input2:
                    run_command_save(["nmap", ip_addr], scan)

                else:
                    # new_input2 = input2.split("")
                    # print(new_input2)
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

                    list_of_commands.append(ip_addr)
                    # print(list_of_commands)
                    # run_command_save(list_of_commands)
                    run_nmap_scan_firewall(list_of_commands)

            else:
                print("\nInvalid IP entered, Please Try again")
        else:
            print("\nUnsupported Option selected, Please Try again")
        time.sleep(0.3)


def menu_windows():
    """Function for Initial Menu to show in front of the user"""
    # check_and_run_admin_windows()
    print("(Windows Version)")
    while True:
        print(r"""
Select an Option:
    [1] Scan full network (find specific host)
    [2] Ping custom IP
    [3] Trace routing
    [4] Advanced scan (single IP)
    [5] Advanced scan (IP range)
    [6] MAC vendor lookup (online)
    [7] Show network info
    [H] Help        [0] Quit
        """.rstrip())
        input1 = input("Omni-Scanner > ").lower() or '0'
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
            level_4(number_of_ip=0)
        elif input1 == '5':
            level_4(number_of_ip=1)
        elif input1 == '6':
            mac_addr = input(
                "\nEnter MAC Address to look up (eg. 00:00:00:00:00:00)\nOmni-Scanner > ") or "00:00:00:00:00:00"
            if validate_mac(mac_addr):
                print(f"\nMac Vendor is {get_mac_vendor(mac_addr)}")
            else:
                print("\nInvalid MAC Address entered, Please Try again")
        elif input1 == '7':
            run_command_save(["ipconfig"])
        else:
            print("\nUnsupported Option selected, Please Try again")
        time.sleep(0.3)


if __name__ == "__main__":
    # This file is not meant to be run directly
    # It should be imported and used in main.py
    # If this file is run directly, it will print an error message
    print("Wrong file selected for running\nPlease run 'main.py' file by using 'python main.py' command")
