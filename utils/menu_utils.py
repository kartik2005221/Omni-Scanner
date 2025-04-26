import ipaddress
import re
import subprocess
import sys
import threading
import time

import requests

from utils.common_utils import run_command_save


def validate_ip(ip):
    """To validate the IP address.
    Return True if valid, else False
    :param ip: IP address to validate
    :returns: True if valid, else False"""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def validate_ip_range(ip_range):
    """To validate IP address range. Return True if valid, else False
    :param ip_range: IP address range to validate
    :returns: True if valid, else False"""
    try:
        if "-" in ip_range:
            # noinspection PyTupleAssignmentBalance
            base_ip, start, end = ip_range.rsplit(".", 1)[0], *ip_range.split("-")
            return validate_ip(start) and validate_ip(base_ip + "." + end) and (int(start.split(".")[-1]) <= int(end))
        else:
            return validate_ip(ip_range)
    except ValueError:
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
        process.terminate()  # Kill Nmap process if the user presses Ctrl+C
        print("\nStopping...")


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
        choice = input("\nHost may be blocking ping probes. Press 0 to retry with firewall Bypass option? "
                       "\n::: ").strip().lower()
        if choice == '0':
            new_command = command + ['-Pn']
            # print(f"Running command: {' '.join(new_command)}")
            # subprocess.run(new_command)
            run_command_save(new_command, scan_type="nmap-scan")
        else:
            print("Okay, Exiting...")


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
