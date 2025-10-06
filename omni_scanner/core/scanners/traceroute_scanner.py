"""
Traceroute Scanner - Network path analysis.
"""
import subprocess
import json
from typing import List, Dict, Optional, Tuple
from ..commands.builders import build_traceroute_cmd, get_os_type
from ...utils.logging import get_logger

logger = get_logger(__name__)


class TracerouteScanner:
    """Traceroute scanner for network path analysis."""
    
    def __init__(self):
        self.scan_type = "traceroute"
        
    def scan(self, target: str, max_hops: int = 30, timeout: int = 5) -> Tuple[bool, str, Dict]:
        """
        Perform traceroute scan.
        
        Args:
            target: Target IP or hostname
            max_hops: Maximum number of hops
            timeout: Timeout per hop in seconds
            
        Returns:
            Tuple[bool, str, Dict]: (success, output, results)
        """
        try:
            # Build command
            cmd = build_traceroute_cmd(target, max_hops, timeout)
            logger.info(f"Executing traceroute scan: {' '.join(cmd)}")
            
            # Execute command
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=max_hops*timeout+30)
            
            if result.returncode == 0:
                logger.info("Traceroute scan completed successfully")
                parsed_results = self._parse_output(result.stdout, target)
                return True, result.stdout, parsed_results
            else:
                logger.warning(f"Traceroute scan had issues: {result.stderr}")
                parsed_results = self._parse_output(result.stdout, target)
                return False, result.stdout, parsed_results
                
        except subprocess.TimeoutExpired:
            logger.error("Traceroute scan timed out")
            return False, "Scan timed out", {}
        except Exception as e:
            logger.error(f"Traceroute scan error: {str(e)}")
            return False, str(e), {}
    
    def _parse_output(self, output: str, target: str) -> Dict:
        """Parse traceroute output."""
        lines = output.strip().split('\n')
        hops = []
        
        for line in lines:
            if line.strip() and not line.startswith('traceroute'):
                # Parse hop information
                parts = line.split()
                if len(parts) >= 2 and parts[0].isdigit():
                    hop_num = int(parts[0])
                    hop_ip = parts[1] if len(parts) > 1 else 'unknown'
                    hop_time = 'unknown'
                    
                    # Extract timing information
                    for part in parts:
                        if 'ms' in part:
                            hop_time = part.replace('ms', '')
                            break
                    
                    hops.append({
                        'hop': hop_num,
                        'ip': hop_ip,
                        'time': hop_time
                    })
        
        return {
            'scan_type': 'traceroute',
            'target': target,
            'total_hops': len(hops),
            'hops': hops,
            'destination_reached': any(hop['ip'] == target for hop in hops),
            'timestamp': subprocess.run(['date'], capture_output=True, text=True).stdout.strip()
        }