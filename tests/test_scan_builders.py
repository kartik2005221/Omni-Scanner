"""
Test suite for scan builder functions.
Tests command generation for different scan types and platforms.
"""
import unittest
import sys
import os
from unittest.mock import patch

# Add the parent directory to the path to import utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.scan_builders import (
    build_arp_scan_cmd, build_nmap_arp_scan_cmd, build_ping_cmd,
    build_traceroute_cmd, build_nmap_scan_cmd, build_nmap_firewall_scan_cmd,
    get_os_type
)


class TestScanBuilders(unittest.TestCase):
    """Test cases for scan builder functions."""
    
    def test_build_arp_scan_cmd_basic(self):
        """Test basic ARP scan command building."""
        with patch('utils.scan_builders.get_os_type', return_value='linux'):
            cmd = build_arp_scan_cmd(sudo_required=True)
            self.assertIn("sudo", cmd)
            self.assertIn("arp-scan", cmd)
            self.assertIn("-l", cmd)
    
    def test_build_arp_scan_cmd_with_target(self):
        """Test ARP scan with specific target."""
        cmd = build_arp_scan_cmd(target="192.168.1.0/24", sudo_required=False)
        self.assertIn("arp-scan", cmd)
        self.assertIn("192.168.1.0/24", cmd)
        self.assertNotIn("sudo", cmd)
    
    def test_build_arp_scan_cmd_fast(self):
        """Test ARP scan with fast option."""
        cmd = build_arp_scan_cmd(fast=True, sudo_required=False)
        self.assertIn("--timeout", cmd)
        self.assertIn("100", cmd)
    
    def test_build_nmap_arp_scan_cmd(self):
        """Test Nmap ARP scan command building."""
        cmd = build_nmap_arp_scan_cmd("192.168.1.1")
        expected_elements = ["nmap", "-sn", "-T5", "--min-parallelism", "100", "192.168.1.1"]
        for element in expected_elements:
            self.assertIn(element, cmd)
    
    def test_build_ping_cmd_linux(self):
        """Test ping command building for Linux."""
        with patch('utils.scan_builders.get_os_type', return_value='linux'):
            cmd = build_ping_cmd("8.8.8.8", count=5, packet_size=64)
            self.assertIn("ping", cmd)
            self.assertIn("8.8.8.8", cmd)
            self.assertIn("-c", cmd)
            self.assertIn("5", cmd)
            self.assertIn("-s", cmd)
            self.assertIn("64", cmd)
    
    def test_build_ping_cmd_windows(self):
        """Test ping command building for Windows."""
        with patch('utils.scan_builders.get_os_type', return_value='windows'):
            cmd = build_ping_cmd("8.8.8.8", count=5, packet_size=64)
            self.assertIn("ping", cmd)
            self.assertIn("8.8.8.8", cmd)
            self.assertIn("-n", cmd)
            self.assertIn("5", cmd)
            self.assertIn("-l", cmd)
            self.assertIn("64", cmd)
    
    def test_build_ping_cmd_flood(self):
        """Test flood ping command."""
        with patch('utils.scan_builders.get_os_type', return_value='linux'):
            cmd = build_ping_cmd("8.8.8.8", flood=True, sudo_required=True)
            self.assertIn("sudo", cmd)
            self.assertIn("-f", cmd)
    
    def test_build_traceroute_cmd_linux(self):
        """Test traceroute command for Linux."""
        with patch('utils.scan_builders.get_os_type', return_value='linux'):
            cmd = build_traceroute_cmd("8.8.8.8", max_hops=15, timeout=3)
            self.assertIn("traceroute", cmd)
            self.assertIn("8.8.8.8", cmd)
            self.assertIn("-m", cmd)
            self.assertIn("15", cmd)
            self.assertIn("-w", cmd)
            self.assertIn("3", cmd)
    
    def test_build_traceroute_cmd_windows(self):
        """Test traceroute command for Windows."""
        with patch('utils.scan_builders.get_os_type', return_value='windows'):
            cmd = build_traceroute_cmd("8.8.8.8", max_hops=15, timeout=3)
            self.assertIn("tracert", cmd)
            self.assertIn("8.8.8.8", cmd)
            self.assertIn("-h", cmd)
            self.assertIn("15", cmd)
            self.assertIn("-w", cmd)
            self.assertIn("3000", cmd)  # Windows uses milliseconds
    
    def test_build_nmap_scan_cmd_basic(self):
        """Test basic Nmap scan command."""
        cmd = build_nmap_scan_cmd("192.168.1.1")
        self.assertIn("nmap", cmd)
        self.assertIn("192.168.1.1", cmd)
        self.assertIn("-sS", cmd)  # Default SYN scan
    
    def test_build_nmap_scan_cmd_with_ports(self):
        """Test Nmap scan with port specification."""
        cmd = build_nmap_scan_cmd("192.168.1.1", ports="80,443")
        self.assertIn("-p", cmd)
        self.assertIn("80,443", cmd)
    
    def test_build_nmap_scan_cmd_service_detection(self):
        """Test Nmap scan with service detection."""
        cmd = build_nmap_scan_cmd("192.168.1.1", service_detection=True, os_detection=True)
        self.assertIn("-sV", cmd)
        self.assertIn("-O", cmd)
    
    def test_build_nmap_firewall_scan_cmd(self):
        """Test Nmap firewall evasion command."""
        cmd = build_nmap_firewall_scan_cmd("192.168.1.1", ports="80-443")
        self.assertIn("nmap", cmd)
        self.assertIn("-sS", cmd)
        self.assertIn("-f", cmd)  # Fragment packets
        self.assertIn("-D", cmd)  # Decoy scan
        self.assertIn("-p", cmd)
        self.assertIn("80-443", cmd)
    
    def test_get_os_type(self):
        """Test OS type detection."""
        os_type = get_os_type()
        self.assertIn(os_type, ['windows', 'linux'])


if __name__ == '__main__':
    unittest.main()