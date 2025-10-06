"""
Asynchronous scanning utilities with progress tracking.
Provides concurrent scanning capabilities and real-time progress indication.
"""
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional, Callable
from tqdm import tqdm
import subprocess
from pathlib import Path

from utils.logging_utils import get_default_logger
from utils.scan_builders import build_ping_cmd, get_os_type
from utils.menu_utils import validate_ip_addr
from utils.output_formatters import ScanResultFormatter


class AsyncScanner:
    """Handles asynchronous scanning operations with progress tracking."""
    
    def __init__(self, max_workers: int = 50, timeout: float = 5.0):
        self.max_workers = max_workers
        self.timeout = timeout
        self.logger = get_default_logger()
        self.formatter = ScanResultFormatter()
    
    async def ping_sweep_async(
        self, 
        network: str, 
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Perform asynchronous ping sweep of a network range.
        
        Args:
            network: Network in CIDR notation (e.g., '192.168.1.0/24')
            progress_callback: Optional callback function for progress updates
            
        Returns:
            Dict: Scan results with alive hosts
        """
        try:
            import ipaddress
            net = ipaddress.ip_network(network, strict=False)
            hosts = [str(ip) for ip in net.hosts()]
        except ValueError:
            raise ValueError(f"Invalid network: {network}")
        
        results = {
            "scan_type": "async_ping_sweep",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "network": network,
            "alive_hosts": [],
            "dead_hosts": [],
            "summary": {}
        }
        
        self.logger.info(f"Starting async ping sweep of {network} ({len(hosts)} hosts)")
        
        # Use ThreadPoolExecutor for concurrent ping operations
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all ping tasks
            future_to_host = {}
            for host in hosts:
                future = executor.submit(self._ping_single_host, host)
                future_to_host[future] = host
            
            # Process results with progress bar
            with tqdm(total=len(hosts), desc="Ping sweep", unit="hosts") as pbar:
                for future in as_completed(future_to_host):
                    host = future_to_host[future]
                    try:
                        is_alive, response_time = future.result(timeout=self.timeout)
                        
                        if is_alive:
                            results["alive_hosts"].append({
                                "ip": host,
                                "response_time_ms": response_time,
                                "status": "alive"
                            })
                        else:
                            results["dead_hosts"].append({
                                "ip": host,
                                "status": "dead"
                            })
                        
                        # Update progress
                        pbar.update(1)
                        if progress_callback:
                            progress_callback(host, is_alive, response_time)
                    
                    except Exception as e:
                        self.logger.error(f"Error pinging {host}: {e}")
                        results["dead_hosts"].append({
                            "ip": host,
                            "status": "error",
                            "error": str(e)
                        })
                        pbar.update(1)
        
        # Update summary
        results["summary"] = {
            "total_hosts": len(hosts),
            "alive_hosts": len(results["alive_hosts"]),
            "dead_hosts": len(results["dead_hosts"]),
            "success_rate": len(results["alive_hosts"]) / len(hosts) * 100
        }
        
        self.logger.info(f"Ping sweep completed: {len(results['alive_hosts'])}/{len(hosts)} hosts alive")
        return results
    
    def _ping_single_host(self, host: str) -> tuple:
        """
        Ping a single host and return result.
        
        Args:
            host: IP address to ping
            
        Returns:
            tuple: (is_alive, response_time_ms)
        """
        try:
            os_type = get_os_type()
            
            if os_type == "windows":
                cmd = ["ping", "-n", "1", "-w", str(int(self.timeout * 1000)), host]
            else:
                cmd = ["ping", "-c", "1", "-W", str(int(self.timeout)), host]
            
            start_time = time.time()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout + 1
            )
            end_time = time.time()
            
            # Check if ping was successful
            if result.returncode == 0:
                response_time = (end_time - start_time) * 1000  # Convert to ms
                return True, response_time
            else:
                return False, 0.0
        
        except subprocess.TimeoutExpired:
            return False, 0.0
        except Exception as e:
            self.logger.debug(f"Ping error for {host}: {e}")
            return False, 0.0
    
    async def port_scan_async(
        self, 
        host: str, 
        ports: List[int], 
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Perform asynchronous port scan on a single host.
        
        Args:
            host: Target IP address
            ports: List of ports to scan
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dict: Port scan results
        """
        if not validate_ip_addr(host):
            raise ValueError(f"Invalid host: {host}")
        
        results = {
            "scan_type": "async_port_scan",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "host": host,
            "open_ports": [],
            "closed_ports": [],
            "summary": {}
        }
        
        self.logger.info(f"Starting async port scan of {host} ({len(ports)} ports)")
        
        # Use ThreadPoolExecutor for concurrent port scanning
        with ThreadPoolExecutor(max_workers=min(self.max_workers, len(ports))) as executor:
            # Submit all port scan tasks
            future_to_port = {}
            for port in ports:
                future = executor.submit(self._scan_single_port, host, port)
                future_to_port[future] = port
            
            # Process results with progress bar
            with tqdm(total=len(ports), desc=f"Port scan {host}", unit="ports") as pbar:
                for future in as_completed(future_to_port):
                    port = future_to_port[future]
                    try:
                        is_open, response_time = future.result(timeout=self.timeout)
                        
                        if is_open:
                            results["open_ports"].append({
                                "port": port,
                                "state": "open",
                                "response_time_ms": response_time
                            })
                        else:
                            results["closed_ports"].append({
                                "port": port,
                                "state": "closed"
                            })
                        
                        # Update progress
                        pbar.update(1)
                        if progress_callback:
                            progress_callback(port, is_open, response_time)
                    
                    except Exception as e:
                        self.logger.error(f"Error scanning port {port}: {e}")
                        pbar.update(1)
        
        # Update summary
        results["summary"] = {
            "total_ports": len(ports),
            "open_ports": len(results["open_ports"]),
            "closed_ports": len(results["closed_ports"])
        }
        
        self.logger.info(f"Port scan completed: {len(results['open_ports'])}/{len(ports)} ports open")
        return results
    
    def _scan_single_port(self, host: str, port: int) -> tuple:
        """
        Scan a single port and return result.
        
        Args:
            host: Target IP address
            port: Port number to scan
            
        Returns:
            tuple: (is_open, response_time_ms)
        """
        try:
            import socket
            
            start_time = time.time()
            
            # Create socket and attempt connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            try:
                result = sock.connect_ex((host, port))
                end_time = time.time()
                
                if result == 0:
                    response_time = (end_time - start_time) * 1000
                    return True, response_time
                else:
                    return False, 0.0
            
            finally:
                sock.close()
        
        except Exception as e:
            self.logger.debug(f"Port scan error for {host}:{port}: {e}")
            return False, 0.0
    
    def save_results_with_progress(
        self, 
        results: Dict[str, Any], 
        filename: str, 
        formats: List[str] = None
    ) -> List[str]:
        """
        Save scan results in multiple formats with progress indication.
        
        Args:
            results: Scan results dictionary
            filename: Base filename (without extension)
            formats: List of formats to export ('json', 'csv', 'html')
            
        Returns:
            List[str]: List of created file paths
        """
        if formats is None:
            formats = ['json']
        
        created_files = []
        
        with tqdm(total=len(formats), desc="Exporting results", unit="files") as pbar:
            for format_type in formats:
                try:
                    if format_type.lower() == 'json':
                        file_path = self.formatter.export_to_json(results, filename)
                    elif format_type.lower() == 'csv':
                        file_path = self.formatter.export_to_csv(results, filename)
                    elif format_type.lower() == 'html':
                        file_path = self.formatter.export_to_html(results, filename)
                    else:
                        self.logger.warning(f"Unsupported format: {format_type}")
                        continue
                    
                    created_files.append(file_path)
                    self.logger.info(f"Results exported to {file_path}")
                    
                except Exception as e:
                    self.logger.error(f"Error exporting to {format_type}: {e}")
                
                pbar.update(1)
        
        return created_files


class ProgressTracker:
    """Utility class for tracking and displaying scan progress."""
    
    def __init__(self):
        self.start_time = time.time()
        self.completed_tasks = 0
        self.total_tasks = 0
        self.logger = get_default_logger()
    
    def start_tracking(self, total_tasks: int, description: str = "Processing"):
        """Start tracking progress for a set of tasks."""
        self.total_tasks = total_tasks
        self.completed_tasks = 0
        self.start_time = time.time()
        self.pbar = tqdm(total=total_tasks, desc=description, unit="tasks")
    
    def update(self, increment: int = 1, description: str = None):
        """Update progress tracker."""
        self.completed_tasks += increment
        self.pbar.update(increment)
        
        if description:
            self.pbar.set_description(description)
    
    def finish(self):
        """Finish progress tracking and show summary."""
        if hasattr(self, 'pbar'):
            self.pbar.close()
        
        duration = time.time() - self.start_time
        rate = self.completed_tasks / duration if duration > 0 else 0
        
        self.logger.info(f"Completed {self.completed_tasks}/{self.total_tasks} tasks in {duration:.2f}s ({rate:.1f} tasks/sec)")


# Convenience functions for common async operations
async def ping_network_range(network: str, max_workers: int = 50) -> Dict[str, Any]:
    """
    Convenience function for async ping sweep.
    
    Args:
        network: Network in CIDR notation
        max_workers: Maximum concurrent workers
        
    Returns:
        Dict: Ping sweep results
    """
    scanner = AsyncScanner(max_workers=max_workers)
    return await scanner.ping_sweep_async(network)


async def scan_host_ports(host: str, ports: List[int], max_workers: int = 50) -> Dict[str, Any]:
    """
    Convenience function for async port scanning.
    
    Args:
        host: Target IP address
        ports: List of ports to scan
        max_workers: Maximum concurrent workers
        
    Returns:
        Dict: Port scan results
    """
    scanner = AsyncScanner(max_workers=max_workers)
    return await scanner.port_scan_async(host, ports)