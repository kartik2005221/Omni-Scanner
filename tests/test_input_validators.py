"""
Unit tests for input_validators module.

These tests validate input parsing and validation logic.
"""

import unittest
from utils.input_validators import (
    parse_port_input,
    validate_packet_size,
    validate_timeout,
    validate_count,
    parse_options_input,
    normalize_ip_network
)


class TestPortValidation(unittest.TestCase):
    """Test port input parsing and validation."""
    
    def test_single_port(self):
        valid, error = parse_port_input("80")
        self.assertTrue(valid)
        self.assertIsNone(error)
    
    def test_comma_separated_ports(self):
        valid, error = parse_port_input("22,80,443")
        self.assertTrue(valid)
        self.assertIsNone(error)
    
    def test_port_range(self):
        valid, error = parse_port_input("1-1000")
        self.assertTrue(valid)
        self.assertIsNone(error)
    
    def test_mixed_ports(self):
        valid, error = parse_port_input("22,80-100,443")
        self.assertTrue(valid)
        self.assertIsNone(error)
    
    def test_invalid_port_number(self):
        valid, error = parse_port_input("70000")
        self.assertFalse(valid)
        self.assertIsNotNone(error)
    
    def test_invalid_range_format(self):
        valid, error = parse_port_input("80-90-100")
        self.assertFalse(valid)
        self.assertIsNotNone(error)
    
    def test_non_numeric_port(self):
        valid, error = parse_port_input("abc")
        self.assertFalse(valid)
        self.assertIsNotNone(error)
    
    def test_empty_input(self):
        valid, error = parse_port_input("")
        self.assertFalse(valid)
        self.assertIsNotNone(error)


class TestPacketSizeValidation(unittest.TestCase):
    """Test packet size validation."""
    
    def test_valid_size(self):
        valid, size = validate_packet_size("1024")
        self.assertTrue(valid)
        self.assertEqual(size, 1024)
    
    def test_minimum_size(self):
        valid, size = validate_packet_size("0")
        self.assertTrue(valid)
        self.assertEqual(size, 0)
    
    def test_maximum_size(self):
        valid, size = validate_packet_size("65500")
        self.assertTrue(valid)
        self.assertEqual(size, 65500)
    
    def test_too_large(self):
        valid, size = validate_packet_size("70000")
        self.assertFalse(valid)
        self.assertIsNone(size)
    
    def test_negative(self):
        valid, size = validate_packet_size("-1")
        self.assertFalse(valid)
        self.assertIsNone(size)
    
    def test_non_numeric(self):
        valid, size = validate_packet_size("abc")
        self.assertFalse(valid)
        self.assertIsNone(size)


class TestTimeoutValidation(unittest.TestCase):
    """Test timeout validation."""
    
    def test_valid_timeout(self):
        valid, timeout = validate_timeout("5")
        self.assertTrue(valid)
        self.assertEqual(timeout, 5)
    
    def test_zero_timeout(self):
        valid, timeout = validate_timeout("0")
        self.assertFalse(valid)
        self.assertIsNone(timeout)
    
    def test_negative_timeout(self):
        valid, timeout = validate_timeout("-1")
        self.assertFalse(valid)
        self.assertIsNone(timeout)


class TestCountValidation(unittest.TestCase):
    """Test packet count validation."""
    
    def test_valid_count(self):
        valid, count = validate_count("10")
        self.assertTrue(valid)
        self.assertEqual(count, 10)
    
    def test_zero_count(self):
        valid, count = validate_count("0")
        self.assertFalse(valid)
        self.assertIsNone(count)


class TestOptionsInput(unittest.TestCase):
    """Test options input parsing."""
    
    def test_valid_single_option(self):
        valid, options = parse_options_input("1", {"1", "2", "3"})
        self.assertTrue(valid)
        self.assertEqual(options, {"1"})
    
    def test_valid_multiple_options(self):
        valid, options = parse_options_input("1 2 3", {"1", "2", "3", "4"})
        self.assertTrue(valid)
        self.assertEqual(options, {"1", "2", "3"})
    
    def test_invalid_option(self):
        valid, options = parse_options_input("1 5", {"1", "2", "3"})
        self.assertFalse(valid)
        self.assertEqual(options, set())
    
    def test_empty_input(self):
        valid, options = parse_options_input("", {"1", "2", "3"})
        self.assertFalse(valid)
        self.assertEqual(options, set())


class TestIPNormalization(unittest.TestCase):
    """Test IP normalization."""
    
    def test_single_ip(self):
        result = normalize_ip_network("192.168.1.1")
        self.assertEqual(result, "192.168.1.1")
    
    def test_subnet_cidr(self):
        result = normalize_ip_network("192.168.1.0/24")
        self.assertEqual(result, "192.168.1.0/24")
    
    def test_ip_range(self):
        result = normalize_ip_network("192.168.1.1-192.168.1.10")
        self.assertEqual(result, "192.168.1.1-192.168.1.10")
    
    def test_short_range(self):
        result = normalize_ip_network("192.168.1.1-10")
        self.assertEqual(result, "192.168.1.1-10")
    
    def test_invalid_ip(self):
        result = normalize_ip_network("999.999.999.999")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
