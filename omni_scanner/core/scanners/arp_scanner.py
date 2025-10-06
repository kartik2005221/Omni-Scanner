"""
ARP Scanner - Device discovery using ARP protocol.
"""
import subprocess
import json
from typing import List, Dict, Optional, Tuple
from ..commands.builders import build_arp_scan_cmd, get_os_type
from ...utils.logging import get_logger

logger = get_logger(__name__)


class ARPScanner:
    """ARP scanner for device discovery."""
    
    def __init__(self):
        self.scan_type = "arp"
        
    def scan(self, target: Optional[str] = None, fast: bool = False, 
             interface: Optional[str] = None) -> Tuple[bool, str, Dict]:
        """
        Perform ARP scan.
        
        Args:
            target: Target network (if None, scans local network)
            fast: Use fast scan options
            interface: Network interface to use
            
        Returns:
            Tuple[bool, str, Dict]: (success, output, results)
        """
        try:
            # Build command
            cmd = build_arp_scan_cmd(target, fast, interface)
            logger.info(f"Executing ARP scan: {' '.join(cmd)}")
            
            # Execute command
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                logger.info("ARP scan completed successfully")
                parsed_results = self._parse_output(result.stdout)
                return True, result.stdout, parsed_results
            else:
                logger.error(f"ARP scan failed: {result.stderr}")
                return False, result.stderr, {}
                
        except subprocess.TimeoutExpired:
            logger.error("ARP scan timed out")
            return False, "Scan timed out", {}
        except Exception as e:
            logger.error(f"ARP scan error: {str(e)}")
            return False, str(e), {}
    
    def _parse_output(self, output: str) -> Dict:
        """Parse ARP scan output."""
        devices = []
        lines = output.strip().split('\n')
        
        for line in lines:
            if '\t' in line or '  ' in line:
                parts = line.split()
                if len(parts) >= 2:
                    devices.append({
                        'ip': parts[0],
                        'mac': parts[1] if len(parts) > 1 else 'Unknown',
                        'vendor': ' '.join(parts[2:]) if len(parts) > 2 else 'Unknown'
                    })
        
        return {
            'scan_type': 'arp',
            'devices_found': len(devices),
            'devices': devices,
            'timestamp': subprocess.run(['date'], capture_output=True, text=True).stdout.strip()
        }