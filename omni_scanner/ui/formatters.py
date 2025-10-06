"""
Output formatting utilities for different export formats.
Supports JSON, CSV, HTML, and summary formats for scan results.
"""
import json
import csv
import html
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import re


class ScanResultFormatter:
    """Handles formatting and export of scan results in various formats."""
    
    def __init__(self):
        self.timestamp = datetime.now()
    
    def parse_nmap_output(self, output: str) -> Dict[str, Any]:
        """
        Parse nmap output into structured data.
        
        Args:
            output: Raw nmap output string
            
        Returns:
            Dict: Structured nmap results
        """
        result = {
            "scan_type": "nmap",
            "timestamp": self.timestamp.isoformat(),
            "hosts": [],
            "summary": {}
        }
        
        lines = output.split('\n')
        current_host = None
        
        for line in lines:
            line = line.strip()
            
            # Parse host information
            if "Nmap scan report for" in line:
                host_info = line.replace("Nmap scan report for ", "")
                current_host = {
                    "address": host_info,
                    "ports": [],
                    "status": "up"
                }
                result["hosts"].append(current_host)
            
            # Parse port information
            elif "/" in line and current_host and ("open" in line or "closed" in line or "filtered" in line):
                port_match = re.match(r'(\d+)/(\w+)\s+(\w+)\s+(.+)', line)
                if port_match:
                    port, protocol, state, service = port_match.groups()
                    current_host["ports"].append({
                        "port": int(port),
                        "protocol": protocol,
                        "state": state,
                        "service": service.strip()
                    })
            
            # Parse summary information
            elif "Nmap done:" in line:
                summary_match = re.search(r'(\d+) IP addresses? \((\d+) hosts? up\)', line)
                if summary_match:
                    total_addresses, hosts_up = summary_match.groups()
                    result["summary"] = {
                        "total_addresses": int(total_addresses),
                        "hosts_up": int(hosts_up),
                        "hosts_down": int(total_addresses) - int(hosts_up)
                    }
        
        return result
    
    def parse_ping_output(self, output: str, target: str) -> Dict[str, Any]:
        """
        Parse ping output into structured data.
        
        Args:
            output: Raw ping output string
            target: Target that was pinged
            
        Returns:
            Dict: Structured ping results
        """
        result = {
            "scan_type": "ping",
            "timestamp": self.timestamp.isoformat(),
            "target": target,
            "packets": [],
            "summary": {}
        }
        
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Parse individual ping responses
            if "time=" in line:
                time_match = re.search(r'time=(\d+\.?\d*)', line)
                ttl_match = re.search(r'ttl=(\d+)', line)
                
                if time_match:
                    packet = {"time_ms": float(time_match.group(1))}
                    if ttl_match:
                        packet["ttl"] = int(ttl_match.group(1))
                    result["packets"].append(packet)
            
            # Parse statistics
            elif "packets transmitted" in line:
                stats_match = re.search(r'(\d+) packets transmitted, (\d+) received', line)
                if stats_match:
                    transmitted, received = stats_match.groups()
                    result["summary"]["packets_transmitted"] = int(transmitted)
                    result["summary"]["packets_received"] = int(received)
                    result["summary"]["packet_loss"] = ((int(transmitted) - int(received)) / int(transmitted)) * 100
            
            elif "min/avg/max" in line:
                time_stats = re.search(r'(\d+\.?\d*)/(\d+\.?\d*)/(\d+\.?\d*)', line)
                if time_stats:
                    min_time, avg_time, max_time = time_stats.groups()
                    result["summary"]["min_time_ms"] = float(min_time)
                    result["summary"]["avg_time_ms"] = float(avg_time)
                    result["summary"]["max_time_ms"] = float(max_time)
        
        return result
    
    def parse_arp_scan_output(self, output: str) -> Dict[str, Any]:
        """
        Parse ARP scan output into structured data.
        
        Args:
            output: Raw ARP scan output string
            
        Returns:
            Dict: Structured ARP scan results
        """
        result = {
            "scan_type": "arp",
            "timestamp": self.timestamp.isoformat(),
            "hosts": [],
            "summary": {}
        }
        
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Parse ARP scan results (IP, MAC, Vendor)
            if re.match(r'\d+\.\d+\.\d+\.\d+', line):
                parts = line.split('\t')
                if len(parts) >= 2:
                    host = {
                        "ip": parts[0],
                        "mac": parts[1]
                    }
                    if len(parts) >= 3:
                        host["vendor"] = parts[2]
                    result["hosts"].append(host)
            
            # Parse summary
            elif "hosts responded" in line:
                count_match = re.search(r'(\d+) hosts? responded', line)
                if count_match:
                    result["summary"]["hosts_found"] = int(count_match.group(1))
        
        return result
    
    def export_to_json(self, data: Dict[str, Any], filename: str) -> str:
        """
        Export data to JSON format.
        
        Args:
            data: Structured scan data
            filename: Base filename (without extension)
            
        Returns:
            str: Path to the created JSON file
        """
        filepath = Path("scans") / f"{filename}.json"
        filepath.parent.mkdir(exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return str(filepath)
    
    def export_to_csv(self, data: Dict[str, Any], filename: str) -> str:
        """
        Export data to CSV format.
        
        Args:
            data: Structured scan data
            filename: Base filename (without extension)
            
        Returns:
            str: Path to the created CSV file
        """
        filepath = Path("scans") / f"{filename}.csv"
        filepath.parent.mkdir(exist_ok=True)
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            
            if data["scan_type"] == "nmap":
                # Header
                writer.writerow(["IP", "Port", "Protocol", "State", "Service"])
                
                # Data
                for host in data.get("hosts", []):
                    for port in host.get("ports", []):
                        writer.writerow([
                            host["address"],
                            port["port"],
                            port["protocol"],
                            port["state"],
                            port["service"]
                        ])
            
            elif data["scan_type"] == "arp":
                # Header
                writer.writerow(["IP", "MAC", "Vendor"])
                
                # Data
                for host in data.get("hosts", []):
                    writer.writerow([
                        host["ip"],
                        host["mac"],
                        host.get("vendor", "")
                    ])
            
            elif data["scan_type"] == "ping":
                # Header
                writer.writerow(["Target", "Packet #", "Time (ms)", "TTL"])
                
                # Data
                for i, packet in enumerate(data.get("packets", []), 1):
                    writer.writerow([
                        data["target"],
                        i,
                        packet["time_ms"],
                        packet.get("ttl", "")
                    ])
        
        return str(filepath)
    
    def export_to_html(self, data: Dict[str, Any], filename: str) -> str:
        """
        Export data to HTML format.
        
        Args:
            data: Structured scan data
            filename: Base filename (without extension)
            
        Returns:
            str: Path to the created HTML file
        """
        filepath = Path("scans") / f"{filename}.html"
        filepath.parent.mkdir(exist_ok=True)
        
        html_content = self._generate_html_report(data)
        
        with open(filepath, 'w') as f:
            f.write(html_content)
        
        return str(filepath)
    
    def _generate_html_report(self, data: Dict[str, Any]) -> str:
        """Generate HTML report from scan data."""
        scan_type = data.get("scan_type", "unknown")
        timestamp = data.get("timestamp", "")
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Omni-Scanner {scan_type.upper()} Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .summary {{ background-color: #e8f4f8; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        .open {{ color: green; font-weight: bold; }}
        .closed {{ color: red; }}
        .filtered {{ color: orange; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Omni-Scanner {scan_type.upper()} Report</h1>
        <p>Generated on: {timestamp}</p>
    </div>
"""
        
        if scan_type == "nmap":
            html_content += self._generate_nmap_html(data)
        elif scan_type == "arp":
            html_content += self._generate_arp_html(data)
        elif scan_type == "ping":
            html_content += self._generate_ping_html(data)
        
        html_content += """
</body>
</html>
"""
        return html_content
    
    def _generate_nmap_html(self, data: Dict[str, Any]) -> str:
        """Generate HTML content for nmap results."""
        content = ""
        
        # Summary
        summary = data.get("summary", {})
        if summary:
            content += f"""
    <div class="summary">
        <h2>Scan Summary</h2>
        <p>Total addresses scanned: {summary.get('total_addresses', 'N/A')}</p>
        <p>Hosts up: {summary.get('hosts_up', 'N/A')}</p>
        <p>Hosts down: {summary.get('hosts_down', 'N/A')}</p>
    </div>
"""
        
        # Host details
        content += """
    <h2>Host Details</h2>
    <table>
        <tr><th>Host</th><th>Port</th><th>Protocol</th><th>State</th><th>Service</th></tr>
"""
        
        for host in data.get("hosts", []):
            for port in host.get("ports", []):
                state_class = port["state"]
                content += f"""
        <tr>
            <td>{html.escape(host['address'])}</td>
            <td>{port['port']}</td>
            <td>{port['protocol']}</td>
            <td class="{state_class}">{port['state']}</td>
            <td>{html.escape(port['service'])}</td>
        </tr>
"""
        
        content += "    </table>"
        return content
    
    def _generate_arp_html(self, data: Dict[str, Any]) -> str:
        """Generate HTML content for ARP scan results."""
        content = ""
        
        # Summary
        summary = data.get("summary", {})
        if summary:
            content += f"""
    <div class="summary">
        <h2>Scan Summary</h2>
        <p>Hosts found: {summary.get('hosts_found', 'N/A')}</p>
    </div>
"""
        
        # Host details
        content += """
    <h2>Discovered Hosts</h2>
    <table>
        <tr><th>IP Address</th><th>MAC Address</th><th>Vendor</th></tr>
"""
        
        for host in data.get("hosts", []):
            content += f"""
        <tr>
            <td>{host['ip']}</td>
            <td>{host['mac']}</td>
            <td>{html.escape(host.get('vendor', ''))}</td>
        </tr>
"""
        
        content += "    </table>"
        return content
    
    def _generate_ping_html(self, data: Dict[str, Any]) -> str:
        """Generate HTML content for ping results."""
        content = ""
        
        # Summary
        summary = data.get("summary", {})
        target = data.get("target", "")
        
        content += f"""
    <div class="summary">
        <h2>Ping Summary for {target}</h2>
"""
        
        if summary:
            content += f"""
        <p>Packets transmitted: {summary.get('packets_transmitted', 'N/A')}</p>
        <p>Packets received: {summary.get('packets_received', 'N/A')}</p>
        <p>Packet loss: {summary.get('packet_loss', 'N/A'):.1f}%</p>
        <p>Min/Avg/Max time: {summary.get('min_time_ms', 'N/A')}/{summary.get('avg_time_ms', 'N/A')}/{summary.get('max_time_ms', 'N/A')} ms</p>
"""
        
        content += """
    </div>
    <h2>Ping Responses</h2>
    <table>
        <tr><th>Packet #</th><th>Time (ms)</th><th>TTL</th></tr>
"""
        
        for i, packet in enumerate(data.get("packets", []), 1):
            content += f"""
        <tr>
            <td>{i}</td>
            <td>{packet['time_ms']}</td>
            <td>{packet.get('ttl', 'N/A')}</td>
        </tr>
"""
        
        content += "    </table>"
        return content
    
    def generate_summary(self, data: Dict[str, Any]) -> str:
        """
        Generate a brief summary of scan results.
        
        Args:
            data: Structured scan data
            
        Returns:
            str: Summary string
        """
        scan_type = data.get("scan_type", "unknown")
        
        if scan_type == "nmap":
            hosts = data.get("hosts", [])
            total_hosts = len(hosts)
            total_open_ports = sum(len([p for p in host.get("ports", []) if p["state"] == "open"]) for host in hosts)
            return f"Nmap scan found {total_hosts} hosts with {total_open_ports} open ports total"
        
        elif scan_type == "arp":
            hosts_found = len(data.get("hosts", []))
            return f"ARP scan discovered {hosts_found} active hosts"
        
        elif scan_type == "ping":
            target = data.get("target", "")
            summary = data.get("summary", {})
            packet_loss = summary.get("packet_loss", 0)
            avg_time = summary.get("avg_time_ms", 0)
            return f"Ping to {target}: {packet_loss:.1f}% packet loss, avg time {avg_time:.1f}ms"
        
        return f"Completed {scan_type} scan"