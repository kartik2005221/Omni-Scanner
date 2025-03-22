import subprocess
import ipaddress
from utils.common_utils import oper_system

def traceroute_all_os():
    """Just a Simple Traceroute Function
    :returns : 0"""
    if oper_system() == "Windows":
        subprocess.run(["tracert", input("Enter IP for traceroute : ")])
        input("Press Enter to continue...")
    else:
        subprocess.run(["traceroute", input("Enter IP for traceroute : ")])
        input("Press Enter to continue...")
    return 0

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
# sample codes for reference
# result = subprocess.run(["arp-scan", "-l"], capture_output=True, text=True)
# print("Output:", result.stdout)
# print("Error:", result.stderr)
# print("Return Code:", result.returncode)
