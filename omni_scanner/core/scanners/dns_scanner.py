"""
DNS Lookup and Reverse DNS Lookup functionality for Omni-Scanner.
"""

import socket
import dns.resolver
import dns.reversename
import ipaddress
from typing import Dict, List, Optional, Tuple
from ..utils.logging import get_logger

logger = get_logger(__name__)


class DNSScanner:
    """DNS and Reverse DNS lookup functionality."""
    
    def __init__(self):
        self.scan_type = "dns"
        
    def forward_lookup(self, hostname: str) -> Tuple[bool, str, Dict]:
        """
        Perform forward DNS lookup (hostname to IP).
        
        Args:
            hostname: The hostname to resolve
            
        Returns:
            Tuple[bool, str, Dict]: (success, output, results)
        """
        try:
            logger.info(f"Performing forward DNS lookup for: {hostname}")
            
            # Basic socket resolution
            try:
                ip_address = socket.gethostbyname(hostname)
                
                # Get all IPs for this hostname
                addr_info = socket.getaddrinfo(hostname, None)
                all_ips = list(set([addr[4][0] for addr in addr_info]))
                
                results = {
                    'scan_type': 'dns_forward',
                    'hostname': hostname,
                    'primary_ip': ip_address,
                    'all_ips': all_ips,
                    'record_count': len(all_ips),
                    'status': 'resolved'
                }
                
                logger.info(f"Forward lookup successful: {hostname} -> {ip_address}")
                return True, f"Resolved {hostname} to {ip_address}", results
                
            except socket.gaierror as e:
                logger.warning(f"Forward lookup failed for {hostname}: {e}")
                results = {
                    'scan_type': 'dns_forward',
                    'hostname': hostname,
                    'error': str(e),
                    'status': 'failed'
                }
                return False, f"Failed to resolve {hostname}: {e}", results
                
        except Exception as e:
            logger.error(f"DNS forward lookup error: {str(e)}")
            return False, str(e), {}
    
    def reverse_lookup(self, ip_address: str) -> Tuple[bool, str, Dict]:
        """
        Perform reverse DNS lookup (IP to hostname).
        
        Args:
            ip_address: The IP address to resolve
            
        Returns:
            Tuple[bool, str, Dict]: (success, output, results)
        """
        try:
            # Validate IP address
            try:
                ipaddress.ip_address(ip_address)
            except ValueError as e:
                return False, f"Invalid IP address: {e}", {}
            
            logger.info(f"Performing reverse DNS lookup for: {ip_address}")
            
            try:
                hostname, aliaslist, ipaddrlist = socket.gethostbyaddr(ip_address)
                
                results = {
                    'scan_type': 'dns_reverse',
                    'ip_address': ip_address,
                    'hostname': hostname,
                    'aliases': aliaslist,
                    'all_ips': ipaddrlist,
                    'status': 'resolved'
                }
                
                logger.info(f"Reverse lookup successful: {ip_address} -> {hostname}")
                return True, f"Resolved {ip_address} to {hostname}", results
                
            except socket.herror as e:
                logger.warning(f"Reverse lookup failed for {ip_address}: {e}")
                results = {
                    'scan_type': 'dns_reverse',
                    'ip_address': ip_address,
                    'error': str(e),
                    'status': 'failed'
                }
                return False, f"No reverse DNS record for {ip_address}", results
                
        except Exception as e:
            logger.error(f"DNS reverse lookup error: {str(e)}")
            return False, str(e), {}
    
    def advanced_dns_lookup(self, hostname: str, record_types: List[str] = None) -> Tuple[bool, str, Dict]:
        """
        Perform advanced DNS lookup with multiple record types.
        
        Args:
            hostname: The hostname to resolve
            record_types: List of DNS record types to query (A, AAAA, MX, NS, TXT, etc.)
            
        Returns:
            Tuple[bool, str, Dict]: (success, output, results)
        """
        if record_types is None:
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
        
        try:
            logger.info(f"Performing advanced DNS lookup for: {hostname}")
            
            results = {
                'scan_type': 'dns_advanced',
                'hostname': hostname,
                'records': {},
                'status': 'partial'
            }
            
            total_records = 0
            
            for record_type in record_types:
                try:
                    answers = dns.resolver.resolve(hostname, record_type)
                    record_data = []
                    
                    for answer in answers:
                        if record_type == 'MX':
                            record_data.append({
                                'priority': answer.preference,
                                'exchange': str(answer.exchange)
                            })
                        elif record_type == 'TXT':
                            record_data.append(str(answer))
                        else:
                            record_data.append(str(answer))
                    
                    results['records'][record_type] = record_data
                    total_records += len(record_data)
                    
                except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
                    # No records of this type
                    continue
                except Exception as e:
                    logger.warning(f"Failed to query {record_type} record for {hostname}: {e}")
                    continue
            
            if total_records > 0:
                results['status'] = 'success'
                results['total_records'] = total_records
                
                output = f"Found {total_records} DNS records for {hostname}"
                logger.info(f"Advanced DNS lookup successful for {hostname}")
                return True, output, results
            else:
                results['status'] = 'no_records'
                return False, f"No DNS records found for {hostname}", results
                
        except dns.resolver.NXDOMAIN:
            logger.warning(f"Domain not found: {hostname}")
            results = {
                'scan_type': 'dns_advanced',
                'hostname': hostname,
                'error': 'Domain not found',
                'status': 'nxdomain'
            }
            return False, f"Domain not found: {hostname}", results
            
        except Exception as e:
            logger.error(f"Advanced DNS lookup error: {str(e)}")
            return False, str(e), {}
    
    def bulk_dns_lookup(self, targets: List[str]) -> Tuple[bool, str, Dict]:
        """
        Perform bulk DNS lookups for multiple targets.
        
        Args:
            targets: List of hostnames or IP addresses
            
        Returns:
            Tuple[bool, str, Dict]: (success, output, results)
        """
        try:
            logger.info(f"Performing bulk DNS lookup for {len(targets)} targets")
            
            results = {
                'scan_type': 'dns_bulk',
                'total_targets': len(targets),
                'successful_lookups': 0,
                'failed_lookups': 0,
                'results': []
            }
            
            for target in targets:
                try:
                    # Determine if target is IP or hostname
                    try:
                        ipaddress.ip_address(target)
                        # It's an IP address - do reverse lookup
                        success, output, lookup_result = self.reverse_lookup(target)
                    except ValueError:
                        # It's a hostname - do forward lookup
                        success, output, lookup_result = self.forward_lookup(target)
                    
                    if success:
                        results['successful_lookups'] += 1
                    else:
                        results['failed_lookups'] += 1
                    
                    results['results'].append(lookup_result)
                    
                except Exception as e:
                    logger.warning(f"Bulk lookup failed for {target}: {e}")
                    results['failed_lookups'] += 1
                    results['results'].append({
                        'target': target,
                        'error': str(e),
                        'status': 'error'
                    })
            
            success_rate = (results['successful_lookups'] / len(targets)) * 100
            output = f"Bulk DNS lookup completed: {results['successful_lookups']}/{len(targets)} successful ({success_rate:.1f}%)"
            
            logger.info(output)
            return True, output, results
            
        except Exception as e:
            logger.error(f"Bulk DNS lookup error: {str(e)}")
            return False, str(e), {}