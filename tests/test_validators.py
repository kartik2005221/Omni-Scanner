"""
Test suite for validation functions.
Tests input validation for IPs, ports, and other parameters.
"""
import unittest
import sys
import os

# Add the parent directory to the path to import utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.menu_utils import (
    validate_ip_addr, validate_ip_range, validate_ip_subnet, validate_ip,
    validate_port, validate_port_range, validate_packet_size, validate_packet_count,
    validate_timeout, sanitize_filename, parse_scan_options
)


class TestValidationFunctions(unittest.TestCase):
    """Test cases for validation functions."""
    
    def test_validate_ip_addr(self):
        """Test IP address validation."""
        # Valid IPv4 addresses
        self.assertTrue(validate_ip_addr("192.168.1.1"))
        self.assertTrue(validate_ip_addr("8.8.8.8"))
        self.assertTrue(validate_ip_addr("127.0.0.1"))
        
        # Invalid IP addresses
        self.assertFalse(validate_ip_addr("256.1.1.1"))
        self.assertFalse(validate_ip_addr("192.168.1"))
        self.assertFalse(validate_ip_addr("not.an.ip.address"))
        self.assertFalse(validate_ip_addr(""))
    
    def test_validate_ip_range(self):
        """Test IP range validation."""
        # Valid ranges
        self.assertTrue(validate_ip_range("192.168.1.1-192.168.1.10"))
        self.assertTrue(validate_ip_range("192.168.1.1-10"))
        
        # Invalid ranges
        self.assertFalse(validate_ip_range("192.168.1.1"))
        self.assertFalse(validate_ip_range("192.168.1.10-192.168.1.1"))  # Start > End
        self.assertFalse(validate_ip_range("invalid-range"))
    
    def test_validate_ip_subnet(self):
        """Test IP subnet validation."""
        # Valid subnets
        self.assertTrue(validate_ip_subnet("192.168.1.0/24"))
        self.assertTrue(validate_ip_subnet("10.0.0.0/8"))
        
        # Invalid subnets
        self.assertFalse(validate_ip_subnet("192.168.1.0"))
        self.assertFalse(validate_ip_subnet("192.168.1.0/33"))
        self.assertFalse(validate_ip_subnet("invalid/24"))
    
    def test_validate_ip(self):
        """Test comprehensive IP validation."""
        # Valid IPs, ranges, and subnets
        self.assertTrue(validate_ip("192.168.1.1"))
        self.assertTrue(validate_ip("192.168.1.1-10"))
        self.assertTrue(validate_ip("192.168.1.0/24"))
        
        # Invalid inputs
        self.assertFalse(validate_ip("invalid"))
        self.assertFalse(validate_ip(""))
    
    def test_validate_port(self):
        """Test port validation."""
        # Valid ports
        self.assertTrue(validate_port("80"))
        self.assertTrue(validate_port("443"))
        self.assertTrue(validate_port("65535"))
        
        # Invalid ports
        self.assertFalse(validate_port("0"))
        self.assertFalse(validate_port("65536"))
        self.assertFalse(validate_port("not_a_port"))
        self.assertFalse(validate_port(""))
    
    def test_validate_port_range(self):
        """Test port range validation."""
        # Valid port ranges
        self.assertTrue(validate_port_range("80"))
        self.assertTrue(validate_port_range("80,443"))
        self.assertTrue(validate_port_range("80-443"))
        self.assertTrue(validate_port_range("1-65535"))
        
        # Invalid port ranges
        self.assertFalse(validate_port_range("0-80"))
        self.assertFalse(validate_port_range("80-65536"))
        self.assertFalse(validate_port_range("443-80"))  # Start > End
        self.assertFalse(validate_port_range(""))
    
    def test_validate_packet_size(self):
        """Test packet size validation."""
        # Valid sizes
        self.assertTrue(validate_packet_size("0"))
        self.assertTrue(validate_packet_size("64"))
        self.assertTrue(validate_packet_size("65500"))
        
        # Invalid sizes
        self.assertFalse(validate_packet_size("-1"))
        self.assertFalse(validate_packet_size("65501"))
        self.assertFalse(validate_packet_size("not_a_number"))
    
    def test_validate_packet_count(self):
        """Test packet count validation."""
        # Valid counts
        self.assertTrue(validate_packet_count("1"))
        self.assertTrue(validate_packet_count("100"))
        
        # Invalid counts
        self.assertFalse(validate_packet_count("0"))
        self.assertFalse(validate_packet_count("-1"))
        self.assertFalse(validate_packet_count("not_a_number"))
    
    def test_validate_timeout(self):
        """Test timeout validation."""
        # Valid timeouts
        self.assertTrue(validate_timeout("1"))
        self.assertTrue(validate_timeout("5.5"))
        self.assertTrue(validate_timeout("0.1"))
        
        # Invalid timeouts
        self.assertFalse(validate_timeout("0"))
        self.assertFalse(validate_timeout("-1"))
        self.assertFalse(validate_timeout("not_a_number"))
    
    def test_sanitize_filename(self):
        """Test filename sanitization."""
        # Test with unsafe characters
        self.assertEqual(sanitize_filename("test<>file"), "test__file")
        self.assertEqual(sanitize_filename("test:file"), "test_file")
        self.assertEqual(sanitize_filename("test/file\\name"), "test_file_name")
        
        # Test with empty/whitespace
        self.assertEqual(sanitize_filename(""), "scan_output")
        self.assertEqual(sanitize_filename("   "), "scan_output")
        
        # Test with valid filename
        self.assertEqual(sanitize_filename("valid_filename"), "valid_filename")
    
    def test_parse_scan_options(self):
        """Test scan options parsing."""
        # Valid options
        self.assertEqual(parse_scan_options("1 2 3"), ["1", "2", "3"])
        self.assertEqual(parse_scan_options("fast slow"), ["fast", "slow"])
        
        # Empty input
        self.assertEqual(parse_scan_options(""), [])
        self.assertEqual(parse_scan_options("   "), [])
        
        # Options with invalid characters
        options = parse_scan_options("1 2@ 3#")
        self.assertIn("1", options)
        self.assertNotIn("2@", options)
        self.assertNotIn("3#", options)


if __name__ == '__main__':
    unittest.main()