"""
Command builder functions for various network scanning tools.

This module contains pure functions that build command lists for different
scanning operations. These functions are OS-agnostic where possible and
separate command construction logic from UI and execution.
"""

from typing import List, Optional


def build_ping_cmd_linux(
    target: str,
    count: Optional[int] = None,
    packet_size: Optional[int] = None,
    timeout: Optional[int] = None,
    flood: bool = False
) -> List[str]:
    """
    Build a ping command for Linux systems.

    :param target: IP address or hostname to ping
    :param count: Number of packets to send (None for infinite)
    :param packet_size: Size of packets in bytes (0-65500)
    :param timeout: Timeout in seconds to wait for response
    :param flood: Whether to use flood ping (requires sudo)
    :return: List of command arguments
    """
    cmd = ["ping"]
    
    if flood:
        cmd.insert(0, "sudo")
        cmd.append("-f")
    
    if packet_size is not None:
        cmd.extend(["-s", str(packet_size)])
    
    if timeout is not None:
        cmd.extend(["-W", str(timeout)])
    
    if count is not None:
        cmd.extend(["-c", str(count)])
    
    cmd.append(target)
    return cmd


def build_ping_cmd_windows(
    target: str,
    count: Optional[int] = None,
    packet_size: Optional[int] = None,
    timeout: Optional[int] = None,
    infinite: bool = False
) -> List[str]:
    """
    Build a ping command for Windows systems.

    :param target: IP address or hostname to ping
    :param count: Number of packets to send (ignored if infinite=True)
    :param packet_size: Size of packets in bytes (0-65500)
    :param timeout: Timeout in milliseconds to wait for response
    :param infinite: Whether to ping indefinitely
    :return: List of command arguments
    """
    cmd = ["ping"]
    
    if packet_size is not None:
        cmd.extend(["-l", str(packet_size)])
    
    if timeout is not None:
        cmd.extend(["-w", str(timeout * 1000)])  # Convert to milliseconds
    
    if infinite:
        cmd.append("-t")
    elif count is not None:
        cmd.extend(["-n", str(count)])
    
    cmd.append(target)
    return cmd


def build_arp_scan_cmd_linux(use_sudo: bool = True) -> List[str]:
    """
    Build an ARP scan command for Linux systems.

    :param use_sudo: Whether to use sudo (required for arp-scan)
    :return: List of command arguments
    """
    if use_sudo:
        return ["sudo", "arp-scan", "-l"]
    return ["arp-scan", "-l"]


def build_nmap_arp_scan_cmd(target: str) -> List[str]:
    """
    Build an Nmap ARP scan command (works on both Linux and Windows).

    :param target: IP address, range, or subnet to scan
    :return: List of command arguments
    """
    return [
        "nmap", "-sn", "-T5", 
        "--min-parallelism", "100", 
        "--host-timeout", "2000ms", 
        target
    ]


def build_traceroute_cmd_linux(
    target: str,
    tcp_mode: bool = False,
    use_sudo: bool = False
) -> List[str]:
    """
    Build a traceroute command for Linux systems.

    :param target: IP address or hostname to trace
    :param tcp_mode: Whether to use TCP mode (requires sudo)
    :param use_sudo: Whether sudo is available
    :return: List of command arguments
    """
    if tcp_mode and use_sudo:
        return ["sudo", "traceroute", "-T", "-O", "info", "-p", "80", target]
    return ["traceroute", target]


def build_nmap_cmd(
    target: str,
    detect_os: bool = False,
    detect_services: bool = False,
    syn_scan: bool = False,
    udp_scan: bool = False,
    aggressive: bool = False,
    no_ping: bool = False,
    disable_arp: bool = False,
    ports: Optional[str] = None,
    top_ports: Optional[int] = None,
    all_ports: bool = False,
    use_sudo: bool = False
) -> List[str]:
    """
    Build an Nmap scan command with various options.

    :param target: IP address, range, or subnet to scan
    :param detect_os: Enable OS detection (-O)
    :param detect_services: Enable service/version detection (-sV)
    :param syn_scan: Enable SYN stealth scan (-sS, requires sudo)
    :param udp_scan: Enable UDP scan (-sU, requires sudo)
    :param aggressive: Enable aggressive scan (-A)
    :param no_ping: Disable ping scan (-Pn)
    :param disable_arp: Disable ARP ping (--disable-arp-ping)
    :param ports: Specific ports to scan (e.g., "22,80,443" or "1-1000")
    :param top_ports: Scan top N ports (e.g., 100)
    :param all_ports: Scan all 65535 ports (-p-)
    :param use_sudo: Whether sudo is available
    :return: List of command arguments
    """
    cmd = []
    
    # Add sudo if needed for certain scan types
    if use_sudo and (syn_scan or udp_scan):
        cmd.append("sudo")
    
    cmd.append("nmap")
    
    # Add scan type flags
    if detect_os:
        cmd.append("-O")
    if detect_services:
        cmd.append("-sV")
    if syn_scan:
        cmd.append("-sS")
    if udp_scan:
        cmd.append("-sU")
    if aggressive:
        cmd.append("-A")
    if no_ping:
        cmd.append("-Pn")
    if disable_arp:
        cmd.append("--disable-arp-ping")
    
    # Add port specifications
    if all_ports:
        cmd.extend(["-p-"])
    elif top_ports is not None:
        cmd.extend(["--top-ports", str(top_ports)])
    elif ports:
        cmd.extend(["-p", ports])
    
    cmd.append(target)
    return cmd
