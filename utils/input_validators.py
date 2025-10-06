"""
Enhanced input validation utilities for network scanning operations.

This module provides robust validation functions using the ipaddress standard
library and other best practices for input validation.
"""

import ipaddress
from typing import Optional, Tuple


def parse_port_input(port_input: str) -> Tuple[bool, Optional[str]]:
    """
    Parse and validate port input string.
    
    Supports formats:
    - Single port: "80"
    - Comma-separated: "22,80,443"
    - Range: "1-1000"
    - Mixed: "22,80-100,443"
    
    :param port_input: Port specification string
    :return: Tuple of (is_valid, error_message)
    """
    if not port_input or not port_input.strip():
        return False, "Port input cannot be empty"
    
    # Split by comma first
    port_parts = [p.strip() for p in port_input.split(',')]
    
    for part in port_parts:
        if '-' in part:
            # Handle range
            range_parts = part.split('-')
            if len(range_parts) != 2:
                return False, f"Invalid range format: {part}"
            
            start, end = range_parts
            if not start.strip().isdigit() or not end.strip().isdigit():
                return False, f"Invalid range: {part} contains non-numeric values"
            
            start_port = int(start.strip())
            end_port = int(end.strip())
            
            if start_port < 1 or start_port > 65535:
                return False, f"Start port {start_port} out of valid range (1-65535)"
            if end_port < 1 or end_port > 65535:
                return False, f"End port {end_port} out of valid range (1-65535)"
            if start_port > end_port:
                return False, f"Invalid range: {part} (start > end)"
        else:
            # Single port
            if not part.isdigit():
                return False, f"Invalid port: {part} is not a number"
            
            port = int(part)
            if port < 1 or port > 65535:
                return False, f"Port {port} out of valid range (1-65535)"
    
    return True, None


def validate_packet_size(size: str) -> Tuple[bool, Optional[int]]:
    """
    Validate packet size input.
    
    :param size: Packet size as string
    :return: Tuple of (is_valid, parsed_size or None)
    """
    try:
        size_int = int(size)
        if 0 <= size_int <= 65500:
            return True, size_int
        return False, None
    except ValueError:
        return False, None


def validate_timeout(timeout: str) -> Tuple[bool, Optional[int]]:
    """
    Validate timeout input.
    
    :param timeout: Timeout in seconds as string
    :return: Tuple of (is_valid, parsed_timeout or None)
    """
    try:
        timeout_int = int(timeout)
        if timeout_int > 0:
            return True, timeout_int
        return False, None
    except ValueError:
        return False, None


def validate_count(count: str) -> Tuple[bool, Optional[int]]:
    """
    Validate packet count input.
    
    :param count: Number of packets as string
    :return: Tuple of (is_valid, parsed_count or None)
    """
    try:
        count_int = int(count)
        if count_int > 0:
            return True, count_int
        return False, None
    except ValueError:
        return False, None


def parse_options_input(user_input: str, valid_options: set) -> Tuple[bool, set]:
    """
    Parse space-separated options input and validate against allowed options.
    
    :param user_input: User input string (e.g., "1 2 4")
    :param valid_options: Set of valid option strings
    :return: Tuple of (is_valid, set of selected options)
    """
    if not user_input or not user_input.strip():
        return False, set()
    
    # Split by space and filter out empty strings
    selected = set(filter(None, user_input.strip().split()))
    
    # Check if all selected options are valid
    invalid = selected - valid_options
    if invalid:
        return False, set()
    
    return True, selected


def normalize_ip_network(ip_input: str) -> Optional[str]:
    """
    Normalize IP network input to CIDR notation if possible.
    
    Handles:
    - Single IP: "192.168.1.1" -> "192.168.1.1"
    - CIDR subnet: "192.168.1.0/24" -> "192.168.1.0/24"
    - IP range: "192.168.1.1-192.168.1.10" -> returns as-is (for nmap)
    
    :param ip_input: IP address, subnet, or range
    :return: Normalized IP notation or None if invalid
    """
    try:
        # Try as single IP
        ipaddress.ip_address(ip_input)
        return ip_input
    except ValueError:
        pass
    
    try:
        # Try as network/subnet
        network = ipaddress.ip_network(ip_input, strict=False)
        return str(network)
    except ValueError:
        pass
    
    # If it contains a dash, it might be a range (valid for nmap)
    if '-' in ip_input:
        # Basic validation of range format
        parts = ip_input.split('-')
        if len(parts) == 2:
            # Could be "192.168.1.1-10" or "192.168.1.1-192.168.1.10"
            # Just verify the first part is a valid IP
            try:
                ipaddress.ip_address(parts[0].strip())
                return ip_input  # Return as-is for nmap to handle
            except ValueError:
                pass
    
    return None
