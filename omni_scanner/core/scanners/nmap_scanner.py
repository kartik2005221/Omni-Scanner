"""
Nmap Scanner - Advanced port scanning and service detection.
"""
import subprocess
import json
import threading
import time
from typing import List, Dict, Optional, Tuple
from ..commands.builders import build_nmap_scan_cmd, get_os_type
from ...utils.logging import get_logger

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

logger = get_logger(__name__)


class NmapScanner:
    """Nmap scanner for port scanning and service detection."""
    
    def __init__(self):
        self.scan_type = "nmap"
        
    def _run_with_progress(self, cmd: List[str], estimated_duration: int = 60) -> Tuple[bool, str]:
        """
        Run nmap command with progress bar.
        
        Args:
            cmd: Command to execute
            estimated_duration: Estimated scan duration in seconds
            
        Returns:
            Tuple[bool, str]: (success, output)
        """
        if not TQDM_AVAILABLE:
            # Fallback to regular execution without progress bar
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return result.returncode == 0, result.stdout if result.returncode == 0 else result.stderr
        
        # Start the process
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Create progress bar
        progress_bar = tqdm(
            total=estimated_duration,
            desc="🔍 Nmap scanning",
            unit="s",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
            ncols=80
        )
        
        output = ""
        start_time = time.time()
        
        try:
            # Update progress bar while process is running
            while process.poll() is None:
                elapsed = int(time.time() - start_time)
                if elapsed < estimated_duration:
                    progress_bar.update(1)
                else:
                    # Process is taking longer than estimated
                    progress_bar.total = elapsed + 10
                    progress_bar.update(1)
                
                time.sleep(1)
            
            # Process completed, get output
            stdout, stderr = process.communicate()
            
            # Complete progress bar
            elapsed = int(time.time() - start_time)
            progress_bar.total = elapsed
            progress_bar.n = elapsed
            progress_bar.set_description("✅ Nmap scan completed")
            progress_bar.close()
            
            if process.returncode == 0:
                return True, stdout
            else:
                return False, stderr
                
        except Exception as e:
            progress_bar.close()
            if process.poll() is None:
                process.terminate()
            return False, str(e)
    
    def _estimate_scan_duration(self, target: str, ports: Optional[str] = None, 
                              top_ports: Optional[int] = None, timing: str = "T4") -> int:
        """
        Estimate scan duration based on parameters.
        
        Args:
            target: Target specification
            ports: Port specification
            top_ports: Number of top ports
            timing: Timing template
            
        Returns:
            Estimated duration in seconds
        """
        base_duration = 30  # Base duration
        
        # Adjust for timing template
        timing_multipliers = {
            "T0": 8.0,   # Paranoid - very slow
            "T1": 4.0,   # Sneaky - slow
            "T2": 2.0,   # Polite - slower
            "T3": 1.5,   # Normal
            "T4": 1.0,   # Aggressive - baseline
            "T5": 0.5    # Insane - fast
        }
        multiplier = timing_multipliers.get(timing, 1.0)
        
        # Adjust for number of ports
        if top_ports:
            if top_ports <= 100:
                port_factor = 1.0
            elif top_ports <= 1000:
                port_factor = 2.0
            else:
                port_factor = 3.0
        elif ports:
            if "," in ports:
                port_factor = 0.5  # Specific ports are faster
            elif "-" in ports:
                try:
                    start, end = ports.split("-")
                    port_count = int(end) - int(start) + 1
                    port_factor = min(port_count / 1000.0, 5.0)
                except:
                    port_factor = 2.0
            else:
                port_factor = 0.5
        else:
            port_factor = 2.0  # Default port scan
        
        # Check if it's a network range
        if "/" in target or "-" in target:
            network_factor = 3.0
        else:
            network_factor = 1.0
        
        estimated = int(base_duration * multiplier * port_factor * network_factor)
        return max(10, min(estimated, 300))  # Between 10s and 5min
        
    def scan(self, target: str, ports: Optional[str] = None, 
             scan_type: str = "syn", service_detection: bool = True,
             timing: str = "T4", top_ports: Optional[int] = None, 
             show_progress: bool = True) -> Tuple[bool, str, Dict]:
        """
        Perform Nmap scan.
        
        Args:
            target: Target IP or hostname
            ports: Port specification (e.g., "80,443,22" or "1-1000")
            scan_type: Type of scan (syn, connect, udp)
            service_detection: Enable service version detection
            timing: Timing template (T0-T5)
            top_ports: Scan top N most common ports (1-65535)
            show_progress: Show progress bar during scan
            
        Returns:
            Tuple[bool, str, Dict]: (success, output, results)
        """
        try:
            # Build command - updated to support top_ports
            cmd = build_nmap_scan_cmd(target, ports, scan_type, service_detection, timing, top_ports)
            logger.info(f"Executing Nmap scan: {' '.join(cmd)}")
            
            if show_progress:
                # Estimate scan duration for progress bar
                estimated_duration = self._estimate_scan_duration(target, ports, top_ports, timing)
                success, output = self._run_with_progress(cmd, estimated_duration)
            else:
                # Execute command without progress bar
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                success = result.returncode == 0
                output = result.stdout if success else result.stderr
            
            if success:
                logger.info("Nmap scan completed successfully")
                parsed_results = self._parse_output(output, target)
                return True, output, parsed_results
            else:
                logger.error(f"Nmap scan failed: {output}")
                return False, output, {}
                
        except subprocess.TimeoutExpired:
            logger.error("Nmap scan timed out")
            return False, "Scan timed out", {}
        except Exception as e:
            logger.error(f"Nmap scan error: {str(e)}")
            return False, str(e), {}
    
    def top_ports_scan(self, target: str, num_ports: int = 100, 
                      timing: str = "T4", service_detection: bool = True) -> Tuple[bool, str, Dict]:
        """
        Perform a top N ports scan.
        
        Args:
            target: Target IP or hostname  
            num_ports: Number of top ports to scan (1-65535)
            timing: Timing template (T0-T5)
            service_detection: Enable service version detection
            
        Returns:
            Tuple[bool, str, Dict]: (success, output, results)
        """
        if num_ports < 1 or num_ports > 65535:
            return False, "Number of ports must be between 1 and 65535", {}
        
        logger.info(f"Performing top {num_ports} ports scan on {target}")
        return self.scan(target, None, "syn", service_detection, timing, num_ports)
    
    def comprehensive_scan(self, target: str, timing: str = "T4") -> Tuple[bool, str, Dict]:
        """
        Perform a comprehensive scan with multiple techniques.
        
        Args:
            target: Target IP or hostname
            timing: Timing template (T0-T5)
            
        Returns:
            Tuple[bool, str, Dict]: (success, output, results)
        """
        logger.info(f"Performing comprehensive scan on {target}")
        
        results = {
            'scan_type': 'nmap_comprehensive',
            'target': target,
            'scans': {}
        }
        
        # Quick top 100 ports scan
        success1, output1, result1 = self.top_ports_scan(target, 100, timing, True)
        results['scans']['top_100'] = result1
        
        # UDP scan on common ports
        success2, output2, result2 = self.scan(target, "53,67,68,69,123,135,137,138,139,161,162,445,514,631,1434,1900,4500,5353", "udp", False, timing)
        results['scans']['udp_common'] = result2
        
        # Service version detection on found ports
        if success1 and result1.get('open_ports'):
            open_ports = [p['port'] for p in result1['ports'] if p['state'] == 'open']
            if open_ports:
                port_list = ','.join(open_ports[:20])  # Limit to first 20 ports
                success3, output3, result3 = self.scan(target, port_list, "syn", True, timing)
                results['scans']['detailed_service'] = result3
        
        overall_success = success1 or success2
        summary = f"Comprehensive scan completed. Top ports: {success1}, UDP: {success2}"
        
        return overall_success, summary, results
    
    def _parse_output(self, output: str, target: str) -> Dict:
        """Parse Nmap output."""
        lines = output.strip().split('\n')
        open_ports = []
        host_status = "unknown"
        
        for line in lines:
            if '/tcp' in line or '/udp' in line:
                parts = line.split()
                if len(parts) >= 2:
                    port_info = parts[0].split('/')
                    if len(port_info) >= 2:
                        port_num = port_info[0]
                        protocol = port_info[1]
                        state = parts[1]
                        service = parts[2] if len(parts) > 2 else 'unknown'
                        
                        open_ports.append({
                            'port': port_num,
                            'protocol': protocol,
                            'state': state,
                            'service': service
                        })
            elif 'host up' in line.lower():
                host_status = "up"
            elif 'host down' in line.lower():
                host_status = "down"
        
        return {
            'scan_type': 'nmap',
            'target': target,
            'host_status': host_status,
            'open_ports_count': len([p for p in open_ports if p['state'] == 'open']),
            'ports': open_ports,
            'timestamp': subprocess.run(['date'], capture_output=True, text=True).stdout.strip()
        }