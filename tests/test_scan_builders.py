"""
Unit tests for scan_builders module.

These tests validate command construction logic without executing commands.
"""

import unittest
from utils.scan_builders import (
    build_ping_cmd_linux,
    build_ping_cmd_windows,
    build_arp_scan_cmd_linux,
    build_nmap_arp_scan_cmd,
    build_traceroute_cmd_linux,
    build_nmap_cmd
)


class TestPingCommandBuilders(unittest.TestCase):
    """Test ping command building for Linux and Windows."""
    
    def test_linux_simple_ping(self):
        cmd = build_ping_cmd_linux("192.168.1.1", count=5)
        self.assertEqual(cmd, ["ping", "-c", "5", "192.168.1.1"])
    
    def test_linux_ping_with_packet_size(self):
        cmd = build_ping_cmd_linux("192.168.1.1", count=3, packet_size=1024)
        self.assertEqual(cmd, ["ping", "-s", "1024", "-c", "3", "192.168.1.1"])
    
    def test_linux_ping_with_timeout(self):
        cmd = build_ping_cmd_linux("192.168.1.1", count=3, timeout=2)
        self.assertEqual(cmd, ["ping", "-W", "2", "-c", "3", "192.168.1.1"])
    
    def test_linux_flood_ping(self):
        cmd = build_ping_cmd_linux("192.168.1.1", flood=True)
        self.assertIn("sudo", cmd)
        self.assertIn("-f", cmd)
        self.assertEqual(cmd[-1], "192.168.1.1")
    
    def test_linux_infinite_ping(self):
        cmd = build_ping_cmd_linux("192.168.1.1")
        self.assertEqual(cmd, ["ping", "192.168.1.1"])
    
    def test_windows_simple_ping(self):
        cmd = build_ping_cmd_windows("192.168.1.1", count=5)
        self.assertEqual(cmd, ["ping", "-n", "5", "192.168.1.1"])
    
    def test_windows_ping_infinite(self):
        cmd = build_ping_cmd_windows("192.168.1.1", infinite=True)
        self.assertIn("-t", cmd)
        self.assertEqual(cmd[-1], "192.168.1.1")
    
    def test_windows_ping_with_packet_size(self):
        cmd = build_ping_cmd_windows("192.168.1.1", count=3, packet_size=1024)
        self.assertEqual(cmd, ["ping", "-l", "1024", "-n", "3", "192.168.1.1"])


class TestArpScanBuilders(unittest.TestCase):
    """Test ARP scan command building."""
    
    def test_linux_arp_scan_with_sudo(self):
        cmd = build_arp_scan_cmd_linux(use_sudo=True)
        self.assertEqual(cmd, ["sudo", "arp-scan", "-l"])
    
    def test_linux_arp_scan_without_sudo(self):
        cmd = build_arp_scan_cmd_linux(use_sudo=False)
        self.assertEqual(cmd, ["arp-scan", "-l"])
    
    def test_nmap_arp_scan(self):
        cmd = build_nmap_arp_scan_cmd("192.168.1.0/24")
        self.assertEqual(cmd[0], "nmap")
        self.assertIn("-sn", cmd)
        self.assertEqual(cmd[-1], "192.168.1.0/24")


class TestTracerouteBuilders(unittest.TestCase):
    """Test traceroute command building."""
    
    def test_standard_traceroute(self):
        cmd = build_traceroute_cmd_linux("8.8.8.8")
        self.assertEqual(cmd, ["traceroute", "8.8.8.8"])
    
    def test_tcp_traceroute_with_sudo(self):
        cmd = build_traceroute_cmd_linux("8.8.8.8", tcp_mode=True, use_sudo=True)
        self.assertIn("sudo", cmd)
        self.assertIn("-T", cmd)
        self.assertEqual(cmd[-1], "8.8.8.8")
    
    def test_tcp_traceroute_without_sudo(self):
        cmd = build_traceroute_cmd_linux("8.8.8.8", tcp_mode=True, use_sudo=False)
        self.assertEqual(cmd, ["traceroute", "8.8.8.8"])


class TestNmapCommandBuilders(unittest.TestCase):
    """Test Nmap command building with various options."""
    
    def test_simple_nmap_scan(self):
        cmd = build_nmap_cmd("192.168.1.1")
        self.assertEqual(cmd, ["nmap", "192.168.1.1"])
    
    def test_nmap_os_detection(self):
        cmd = build_nmap_cmd("192.168.1.1", detect_os=True)
        self.assertIn("-O", cmd)
    
    def test_nmap_service_detection(self):
        cmd = build_nmap_cmd("192.168.1.1", detect_services=True)
        self.assertIn("-sV", cmd)
    
    def test_nmap_syn_scan_with_sudo(self):
        cmd = build_nmap_cmd("192.168.1.1", syn_scan=True, use_sudo=True)
        self.assertIn("sudo", cmd)
        self.assertIn("-sS", cmd)
    
    def test_nmap_udp_scan_with_sudo(self):
        cmd = build_nmap_cmd("192.168.1.1", udp_scan=True, use_sudo=True)
        self.assertIn("sudo", cmd)
        self.assertIn("-sU", cmd)
    
    def test_nmap_aggressive_scan(self):
        cmd = build_nmap_cmd("192.168.1.1", aggressive=True)
        self.assertIn("-A", cmd)
    
    def test_nmap_no_ping(self):
        cmd = build_nmap_cmd("192.168.1.1", no_ping=True)
        self.assertIn("-Pn", cmd)
    
    def test_nmap_specific_ports(self):
        cmd = build_nmap_cmd("192.168.1.1", ports="22,80,443")
        self.assertIn("-p", cmd)
        self.assertIn("22,80,443", cmd)
    
    def test_nmap_top_ports(self):
        cmd = build_nmap_cmd("192.168.1.1", top_ports=100)
        self.assertIn("--top-ports", cmd)
        self.assertIn("100", cmd)
    
    def test_nmap_all_ports(self):
        cmd = build_nmap_cmd("192.168.1.1", all_ports=True)
        self.assertIn("-p-", cmd)
    
    def test_nmap_combined_options(self):
        cmd = build_nmap_cmd(
            "192.168.1.1",
            detect_os=True,
            detect_services=True,
            ports="1-1000"
        )
        self.assertIn("-O", cmd)
        self.assertIn("-sV", cmd)
        self.assertIn("-p", cmd)
        self.assertIn("1-1000", cmd)


if __name__ == '__main__':
    unittest.main()
