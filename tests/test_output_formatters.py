"""
Test suite for output formatters.
Tests parsing and formatting of scan results.
"""
import unittest
import json
import tempfile
import os
import sys
from pathlib import Path

# Add the parent directory to the path to import utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.output_formatters import ScanResultFormatter


class TestOutputFormatters(unittest.TestCase):
    """Test cases for output formatting functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.formatter = ScanResultFormatter()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temporary files
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_parse_nmap_output(self):
        """Test parsing of Nmap output."""
        nmap_output = """
Nmap scan report for 192.168.1.1
Host is up (0.0010s latency).
Not shown: 998 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
443/tcp  open  https

Nmap done: 1 IP address (1 host up) scanned in 2.50 seconds
"""
        
        result = self.formatter.parse_nmap_output(nmap_output)
        
        self.assertEqual(result["scan_type"], "nmap")
        self.assertEqual(len(result["hosts"]), 1)
        
        host = result["hosts"][0]
        self.assertEqual(host["address"], "192.168.1.1")
        self.assertEqual(len(host["ports"]), 3)
        
        # Check specific ports
        ports = {port["port"]: port for port in host["ports"]}
        self.assertIn(22, ports)
        self.assertEqual(ports[22]["state"], "open")
        self.assertEqual(ports[22]["service"], "ssh")
    
    def test_parse_ping_output(self):
        """Test parsing of ping output."""
        ping_output = """
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=118 time=15.2 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=118 time=14.8 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=118 time=15.1 ms

--- 8.8.8.8 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss
rtt min/avg/max/mdev = 14.8/15.0/15.2/0.2 ms
"""
        
        result = self.formatter.parse_ping_output(ping_output, "8.8.8.8")
        
        self.assertEqual(result["scan_type"], "ping")
        self.assertEqual(result["target"], "8.8.8.8")
        self.assertEqual(len(result["packets"]), 3)
        
        # Check summary
        summary = result["summary"]
        self.assertEqual(summary["packets_transmitted"], 3)
        self.assertEqual(summary["packets_received"], 3)
        self.assertEqual(summary["packet_loss"], 0.0)
        self.assertAlmostEqual(summary["min_time_ms"], 14.8)
        self.assertAlmostEqual(summary["max_time_ms"], 15.2)
    
    def test_parse_arp_scan_output(self):
        """Test parsing of ARP scan output."""
        arp_output = """
Interface: eth0, datalink type: EN10MB (Ethernet)
Starting arp-scan 1.9.7 with 256 hosts (https://github.com/royhills/arp-scan)
192.168.1.1	aa:bb:cc:dd:ee:ff	Router Vendor
192.168.1.100	11:22:33:44:55:66	Device Vendor

2 packets received by filter, 0 packets dropped by kernel
Ending arp-scan 1.9.7: 256 hosts scanned in 2.000 seconds (128.00 hosts/sec). 2 hosts responded
"""
        
        result = self.formatter.parse_arp_scan_output(arp_output)
        
        self.assertEqual(result["scan_type"], "arp")
        self.assertEqual(len(result["hosts"]), 2)
        
        # Check specific hosts
        host1 = result["hosts"][0]
        self.assertEqual(host1["ip"], "192.168.1.1")
        self.assertEqual(host1["mac"], "aa:bb:cc:dd:ee:ff")
        self.assertEqual(host1["vendor"], "Router Vendor")
        
        # Check summary
        self.assertEqual(result["summary"]["hosts_found"], 2)
    
    def test_export_to_json(self):
        """Test JSON export functionality."""
        test_data = {
            "scan_type": "test",
            "timestamp": "2023-01-01T12:00:00",
            "hosts": [{"ip": "192.168.1.1", "status": "up"}]
        }
        
        # Create a temporary scans directory
        scans_dir = Path(self.temp_dir) / "scans"
        scans_dir.mkdir(exist_ok=True)
        
        # Temporarily change working directory
        original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
        try:
            filename = "test_export"
            result_file = self.formatter.export_to_json(test_data, filename)
            
            # Check file was created
            self.assertTrue(os.path.exists(result_file))
            
            # Check file content
            with open(result_file, 'r') as f:
                loaded_data = json.load(f)
            
            self.assertEqual(loaded_data["scan_type"], "test")
            self.assertEqual(len(loaded_data["hosts"]), 1)
        
        finally:
            os.chdir(original_cwd)
    
    def test_generate_summary(self):
        """Test summary generation for different scan types."""
        # Test Nmap summary
        nmap_data = {
            "scan_type": "nmap",
            "hosts": [
                {
                    "address": "192.168.1.1",
                    "ports": [
                        {"port": 22, "state": "open"},
                        {"port": 80, "state": "open"},
                        {"port": 443, "state": "closed"}
                    ]
                }
            ]
        }
        
        summary = self.formatter.generate_summary(nmap_data)
        self.assertIn("1 hosts", summary)
        self.assertIn("2 open ports", summary)
        
        # Test ARP summary
        arp_data = {
            "scan_type": "arp",
            "hosts": [{"ip": "192.168.1.1"}, {"ip": "192.168.1.2"}]
        }
        
        summary = self.formatter.generate_summary(arp_data)
        self.assertIn("2 active hosts", summary)
        
        # Test ping summary
        ping_data = {
            "scan_type": "ping",
            "target": "8.8.8.8",
            "summary": {
                "packet_loss": 0.0,
                "avg_time_ms": 15.0
            }
        }
        
        summary = self.formatter.generate_summary(ping_data)
        self.assertIn("8.8.8.8", summary)
        self.assertIn("0.0% packet loss", summary)
        self.assertIn("15.0ms", summary)


if __name__ == '__main__':
    unittest.main()