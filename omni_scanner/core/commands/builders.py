"""
Command builders for various network scanning operations.
These functions build command lists for different scan types while maintaining security and consistency.
"""
import platform
from typing import List, Optional


def get_os_type() -> str:
    """Get the current operating system type."""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system in ["linux", "darwin"]:
        return "linux"
    else:
        return "linux"  # Default fallback


def build_arp_scan_cmd(
    target: Optional[str] = None,
    fast: bool = False,
    interface: Optional[str] = None,
    sudo_required: bool = True
) -> List[str]:
    """
    Build ARP scan command.
    
    Args:
        target: Target network (if None, scans local network)
        fast: Use fast scan options
        interface: Network interface to use
        sudo_required: Whether sudo is required
        
    Returns:
        List[str]: Command arguments for ARP scan
    """
    cmd = []
    
    if sudo_required and get_os_type() == "linux":
        cmd.append("sudo")
    
    cmd.extend(["arp-scan"])
    
    if target:
        cmd.append(target)
    else:
        cmd.append("-l")  # Local network scan
    
    if fast:
        cmd.extend(["--timeout", "100"])
    
    if interface:
        cmd.extend(["--interface", interface])
    
    return cmd


def build_nmap_arp_scan_cmd(
    target: str,
    timing: str = "T5",
    min_parallelism: int = 100,
    host_timeout: str = "2000ms"
) -> List[str]:
    """
    Build Nmap ARP scan command.
    
    Args:
        target: Target IP or network
        timing: Nmap timing template (T0-T5)
        min_parallelism: Minimum parallel operations
        host_timeout: Host timeout value
        
    Returns:
        List[str]: Command arguments for Nmap ARP scan
    """
    cmd = [
        "nmap",
        "-sn",  # Ping scan only
        f"-{timing}",
        "--min-parallelism", str(min_parallelism),
        "--host-timeout", host_timeout,
        target
    ]
    
    return cmd


def build_ping_cmd(
    target: str,
    count: Optional[int] = None,
    packet_size: Optional[int] = None,
    timeout: Optional[float] = None,
    flood: bool = False,
    infinite: bool = False,
    sudo_required: bool = False
) -> List[str]:
    """
    Build ping command for different operating systems.
    
    Args:
        target: Target IP address
        count: Number of packets to send
        packet_size: Size of packets in bytes
        timeout: Timeout in seconds
        flood: Enable flood ping (requires sudo)
        infinite: Ping infinitely
        sudo_required: Whether sudo is available/required
        
    Returns:
        List[str]: Command arguments for ping
    """
    cmd = []
    os_type = get_os_type()
    
    # Add sudo for flood ping on Linux
    if flood and os_type == "linux" and sudo_required:
        cmd.append("sudo")
    
    # Base ping command
    if os_type == "windows":
        cmd.append("ping")
    else:
        cmd.append("ping")
    
    # Add target
    cmd.append(target)
    
    # Add options based on OS
    if os_type == "windows":
        if count and not infinite:
            cmd.extend(["-n", str(count)])
        if packet_size:
            cmd.extend(["-l", str(packet_size)])
        if timeout:
            cmd.extend(["-w", str(int(timeout * 1000))])  # Windows uses milliseconds
    else:  # Linux/Unix
        if count and not infinite:
            cmd.extend(["-c", str(count)])
        if packet_size:
            cmd.extend(["-s", str(packet_size)])
        if timeout:
            cmd.extend(["-W", str(int(timeout))])  # Linux uses seconds
        if flood and sudo_required:
            cmd.append("-f")
    
    return cmd


def build_traceroute_cmd(
    target: str,
    max_hops: Optional[int] = None,
    timeout: Optional[float] = None,
    port: Optional[int] = None
) -> List[str]:
    """
    Build traceroute command for different operating systems.
    
    Args:
        target: Target IP address or hostname
        max_hops: Maximum number of hops
        timeout: Timeout per hop in seconds
        port: Port to use for tracing
        
    Returns:
        List[str]: Command arguments for traceroute
    """
    os_type = get_os_type()
    
    if os_type == "windows":
        cmd = ["tracert"]
        if max_hops:
            cmd.extend(["-h", str(max_hops)])
        if timeout:
            cmd.extend(["-w", str(int(timeout * 1000))])  # Windows uses milliseconds
        cmd.append(target)
    else:  # Linux/Unix
        cmd = ["traceroute"]
        if max_hops:
            cmd.extend(["-m", str(max_hops)])
        if timeout:
            cmd.extend(["-w", str(int(timeout))])
        if port:
            cmd.extend(["-p", str(port)])
        cmd.append(target)
    
    return cmd


def build_nmap_scan_cmd(
    target: str,
    scan_type: str = "syn",
    ports: Optional[str] = None,
    os_detection: bool = False,
    service_detection: bool = False,
    timing: str = "T4",
    output_format: str = "normal",
    top_ports: Optional[int] = None
) -> List[str]:
    """
    Build Nmap scan command with various options.
    
    Args:
        target: Target IP address or network
        scan_type: Type of scan (syn, tcp, udp, etc.)
        ports: Port specification (e.g., "80,443", "1-1000")
        os_detection: Enable OS detection
        service_detection: Enable service/version detection
        timing: Timing template (T0-T5)
        output_format: Output format
        top_ports: Scan top N most common ports
        
    Returns:
        List[str]: Command arguments for Nmap scan
    """
    cmd = ["nmap"]
    
    # Scan type
    scan_types = {
        "syn": "-sS",
        "tcp": "-sT",
        "udp": "-sU",
        "ping": "-sn",
        "ack": "-sA",
        "window": "-sW",
        "null": "-sN",
        "fin": "-sF",
        "xmas": "-sX"
    }
    
    if scan_type in scan_types:
        cmd.append(scan_types[scan_type])
    
    # Port specification - top_ports takes precedence over ports
    if top_ports is not None and 1 <= top_ports <= 65535:
        cmd.extend(["--top-ports", str(top_ports)])
    elif ports:
        cmd.extend(["-p", ports])
    
    # Additional options
    if os_detection:
        cmd.append("-O")
    
    if service_detection:
        cmd.append("-sV")
    
    # Timing
    if timing in ["T0", "T1", "T2", "T3", "T4", "T5"]:
        cmd.append(f"-{timing}")
    
    # Target
    cmd.append(target)
    
    return cmd


def build_nmap_firewall_scan_cmd(
    target: str,
    ports: Optional[str] = None,
    timing: str = "T4"
) -> List[str]:
    """
    Build Nmap firewall evasion scan command.
    
    Args:
        target: Target IP address
        ports: Port specification
        timing: Timing template
        
    Returns:
        List[str]: Command arguments for firewall scan
    """
    cmd = [
        "nmap",
        "-sS",  # SYN scan
        "-f",   # Fragment packets
        "-D", "RND:10",  # Decoy scan
        f"-{timing}"
    ]
    
    if ports:
        cmd.extend(["-p", ports])
    
    cmd.append(target)
    return cmd