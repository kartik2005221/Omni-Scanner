"""
Ping Scanner - Network connectivity testing.
"""
import subprocess
import json
from typing import List, Dict, Optional, Tuple
from ..commands.builders import build_ping_cmd, get_os_type
from ...utils.logging import get_logger

logger = get_logger(__name__)


class PingScanner:
    """Ping scanner for connectivity testing."""
    
    def __init__(self):
        self.scan_type = "ping"
        
    def scan(self, target: str, count: int = 4, packet_size: int = 64, 
             timeout: int = 5) -> Tuple[bool, str, Dict]:
        """
        Perform ping scan.
        
        Args:
            target: Target IP or hostname
            count: Number of ping packets
            packet_size: Size of ping packets
            timeout: Timeout in seconds
            
        Returns:
            Tuple[bool, str, Dict]: (success, output, results)
        """
        try:
            # Build command
            cmd = build_ping_cmd(target, count, packet_size, timeout)
            logger.info(f"Executing ping scan: {' '.join(cmd)}")
            
            # Execute command
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout+10)
            
            if result.returncode == 0:
                logger.info("Ping scan completed successfully")
                parsed_results = self._parse_output(result.stdout, target)
                return True, result.stdout, parsed_results
            else:
                logger.warning(f"Ping scan had issues: {result.stderr}")
                parsed_results = self._parse_output(result.stdout, target)
                return False, result.stdout, parsed_results
                
        except subprocess.TimeoutExpired:
            logger.error("Ping scan timed out")
            return False, "Scan timed out", {}
        except Exception as e:
            logger.error(f"Ping scan error: {str(e)}")
            return False, str(e), {}
    
    def _parse_output(self, output: str, target: str) -> Dict:
        """Parse ping output."""
        lines = output.strip().split('\n')
        packets_sent = 0
        packets_received = 0
        avg_time = 0
        
        for line in lines:
            if 'packets transmitted' in line.lower():
                parts = line.split()
                for i, part in enumerate(parts):
                    if 'transmitted' in part and i > 0:
                        packets_sent = int(parts[i-1])
                    if 'received' in part and i > 0:
                        packets_received = int(parts[i-1])
            elif 'avg' in line.lower() or 'average' in line.lower():
                if 'ms' in line:
                    avg_time = float(line.split('/')[-2])
        
        packet_loss = ((packets_sent - packets_received) / max(packets_sent, 1)) * 100
        
        return {
            'scan_type': 'ping',
            'target': target,
            'packets_sent': packets_sent,
            'packets_received': packets_received,
            'packet_loss_percent': packet_loss,
            'average_time_ms': avg_time,
            'reachable': packets_received > 0,
            'timestamp': subprocess.run(['date'], capture_output=True, text=True).stdout.strip()
        }