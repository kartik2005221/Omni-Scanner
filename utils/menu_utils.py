import ipaddress
import re
import subprocess
import sys
import threading
import time

import requests

from utils.common_utils import run_command_save, shell


def validate_ip_addr(ip_addr):
    """To validate the IP address.
    Return True if valid, else False
    :param ip_addr: IP address to validate
    :returns bool: True if valid, else False
    """
    try:
        ipaddress.ip_address(ip_addr)
        return True
    except ValueError:
        return False


def validate_ip_range(ip_range):
    """
    Validates if a given string represents a valid IP range.
    :param ip_range: The string representation of the IP range
    :return: True if valid, False otherwise
    """
    try:
        if "-" not in ip_range:
            return False

        # full range like 192.168.0.1-192.168.0.10
        if "." in ip_range.split("-")[1]:
            start_ip, end_ip = ip_range.split("-")
            if validate_ip_addr(start_ip) and validate_ip_addr(end_ip):
                return int(ipaddress.IPv4Address(start_ip)) <= int(ipaddress.IPv4Address(end_ip))
            return False

        # compressed format like 192.168.0.1-10
        full_part, short_end = ip_range.split("-")
        ip_parts = full_part.split(".")
        if len(ip_parts) != 4:
            return False

        base = ".".join(ip_parts[:3])
        start = int(ip_parts[3])
        end = int(short_end)

        start_ip = f"{base}.{start}"
        end_ip = f"{base}.{end}"

        if validate_ip_addr(start_ip) and validate_ip_addr(end_ip):
            return start <= end
        return False

    except ValueError:
        return False


def validate_ip_subnet(ip_subnet):
    """Validates if a given string represents a valid IP subnet.
    :param ip_subnet: The string representation of the IP subnet (e.g., "192.168.1.0/24").
    :return bool: True if valid, False otherwise.
    """
    try:
        ipaddress.ip_network(ip_subnet, strict=True)
        return True
    except ValueError:
        return False


def validate_ip(ip):
    """
    Validates if a given string is a valid IP address, IP range, or IP subnet.
    :param ip: The ip address or range or subnet to validate
    :return: True if valid, False otherwise
    """
    if validate_ip_addr(ip) or validate_ip_range(ip) or validate_ip_subnet(ip):
        return True
    else:
        return False


def spinning_cursor():
    """Generator for spinning cursor"""
    while True:
        for cursor in '|/-\\':
            yield cursor


def spinner_task(spinner_user):
    """Displays a spinner while the process is running"""
    spinner = spinning_cursor()
    while spinner_user.poll() is None:  # Keep running while a process is active
        sys.stdout.write(f"\rScanning network... {next(spinner)} ")
        sys.stdout.flush()
        time.sleep(0.2)  # Adjust the speed of the spinner
    # sys.stdout.write("\rScanning complete!     \n")


process = 0


def insert_spinner(command):
    """Runs Nmap scan with progress indicator and graceful exit"""
    for i in command:
        print(i, end=" ")
    print()
    global process
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Start the spinner in a separate thread
        spinner_thread = threading.Thread(target=spinner_task, args=(process,), daemon=True)
        spinner_thread.start()
        # Wait for the Nmap process to complete
        stdout, stderr = process.communicate()
        # Print Nmap results
        print("\n \n", stdout)
        if stderr:
            print("\nErrors:\n", stderr)
    except KeyboardInterrupt:
        process.terminate()
        print("\nStopping...")
    else:
        input("Press Enter to continue...")
        time.sleep(0.3)


def get_mac_vendor(mac_address: str) -> str:
    url = f"https://api.macvendors.com/{mac_address}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text.strip()
        elif response.status_code == 404:
            return "Vendor Not Found"
        elif response.status_code == 429:
            return ("Rate Limit Exceeded. Try again later.\n\tOR\nTry Paid API for more requests "
                    "https://macvendors.com/plans")
        else:
            return f"Error: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Request Error: {str(e)}"


def validate_mac(mac: str) -> bool:
    """
    Validates a MAC address in various formats.
    Supports:
    - XX:XX:XX:XX:XX:XX
    - XX-XX-XX-XX-XX-XX
    - XXXXXXXXXXXX
    - XXXX.XXXX.XXXX
    :param mac: MAC address to validate
    :returns: True if valid, else False
    """
    mac = mac.strip()
    patterns = [
        r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',  # 00:11:22:33:44:55 or 00-11-22-33-44-55
        r'^([0-9A-Fa-f]{12})$',  # 001122334455
        r'^([0-9A-Fa-f]{4}\.){2}[0-9A-Fa-f]{4}$'  # 0011.2233.4455
    ]

    for pattern in patterns:
        if re.match(pattern, mac):
            return True
    return False


def run_tcp_traceroute_windows(target):
    """Runs TCP-based traceroute using Nmap on Windows
    :param target: Target IP address or hostname
    :returns: None"""
    print(f"\nRunning TCP-based traceroute to {target}...\n")
    try:
        result = subprocess.run(
            ['nmap', '--traceroute', '-p', '80', target],
            capture_output=True,
            text=True
        )

        output = result.stdout
        if "TRACEROUTE" not in output:
            print("Traceroute data not found in Nmap output. Make sure target is up and port 80 is open.")
            return

        print("Traceroute Path:\n")
        in_traceroute = False

        for line in output.splitlines():
            if "TRACEROUTE" in line:
                in_traceroute = True
                continue
            elif in_traceroute:
                if line.strip() == "":
                    break  # End of the traceroute section

                match = re.match(r'^\s*(\d+)\s+([\d.]+)\s+(.+)$', line)
                if match:
                    hop = match.group(1)
                    rtt = match.group(2)
                    address = match.group(3)
                    print(f"Hop {hop}: {rtt} - {address}")
    except Exception as e:
        print(f"Error running traceroute: {e}")


def run_nmap_scan_firewall(command):
    """Runs Nmap scan with a firewall bypass option whenever required
    :param command: Nmap command to run
    :returns: None"""
    print(f"Executing: {' '.join(command)}")
    proces = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,  # Line-buffered
        universal_newlines=True
    )

    host_down_detected = False
    while True:
        line = proces.stdout.readline()
        if not line and proces.poll() is not None:
            break  # Exit loop when a process finishes
        print(line, end='')  # Print live output
        if "Note: Host seems down" in line:
            host_down_detected = True
    if host_down_detected:
        choice = input("\nHost may be blocking ping probes. Press 0 to retry with firewall Bypass option? \n" +
                       shell).strip().lower()
        if choice == '0':
            new_command = command + ['-Pn']
            # print(f"Running command: {' '.join(new_command)}")
            # subprocess.run(new_command)
            run_command_save(new_command, scan_type="nmap-scan")
        else:
            print("Okay, Exiting...")


def validate_port(port):
    """
    Validate the port number.

    :param port: Port number to validate
    :return: True if valid, False otherwise
    """
    ports_list = []

    # Split the input based on ',' and '-'
    if "," in port:
        ports = port.split(",")
        for p in ports:
            if "-" in p:
                sub_ports = p.split("-")
                if len(sub_ports) != 2:
                    print(f"Invalid range format: {p}")
                    return False
                start, end = sub_ports
                if not start.strip().isdigit() or not end.strip().isdigit():
                    print(f"Invalid range: {p} contains non-numeric values")
                    return False
                if int(start.strip()) > int(end.strip()):
                    print(f"Invalid range: {p} start is greater than end")
                    return False
                ports_list.extend(sub_ports)
            else:
                ports_list.append(p.strip())
    elif "-" in port:
        sub_ports = port.split("-")
        if len(sub_ports) != 2:
            print(f"Invalid range format: {port}")
            return False
        start, end = sub_ports
        if not start.strip().isdigit() or not end.strip().isdigit():
            print(f"Invalid range: {port} contains non-numeric values")
            return False
        if int(start.strip()) > int(end.strip()):
            print(f"Invalid range: {port} start is greater than end")
            return False
        ports_list.extend(sub_ports)
    else:
        ports_list.append(port.strip())

    print(ports_list)

    # Validate each port in the list
    for p in ports_list:
        if not p.isdigit():
            print(f"Invalid port: {p} is not a number")
            return False
        if not (1 <= int(p) <= 65535):
            print(f"Invalid port: {p} is out of range (1-65535)")
            return False
    return True


# import importlib.util
# def is_module_installed(module_name):
#     """Check if a module is installed
#     :param module_name: Name of the module to check
#     :returns : True if installed, else False"""
#     spec = importlib.util.find_spec(module_name)
#     return spec is not None
#

# def get_ip():
#     """Get the IP address of the current system"""
#     if oper_system() == "Windows":
#         run_command(["ipconfig"])
#     else:
#         run_command(["ip", "addr"])


# sample codes for reference
# result = run_command(["arp-scan", "-l"], capture_output=True, text=True)
# print("Output:", result.stdout)
# print("Error:", result.stderr)
# print("Return Code:", result.returncode)
if __name__ == "__main__":
    # This file is not meant to be run directly
    # It should be imported and used in main.py
    # If this file is run directly, it will print an error message
    print("Wrong file selected for running\nPlease run 'main.py' file by using 'python main.py' command")