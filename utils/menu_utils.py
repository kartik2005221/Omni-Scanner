import subprocess
from utils.common_utils import oper_system

def traceroute_all_os():
    """Just a Simple Traceroute Function"""
    if oper_system() == "Windows":
        subprocess.run(["tracert", input("Enter IP for traceroute : ")])
    else:
        subprocess.run(["traceroute", input("Enter IP for traceroute : ")])
    return 0

# sample codes for reference
# result = subprocess.run(["arp-scan", "-l"], capture_output=True, text=True)
# print("Output:", result.stdout)
# print("Error:", result.stderr)
# print("Return Code:", result.returncode)
