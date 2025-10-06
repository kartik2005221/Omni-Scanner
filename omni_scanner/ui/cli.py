"""
Modern CLI interface for Omni-Scanner using Typer.
Provides subcommands for different scan types while maintaining backwards compatibility.
"""
import typer
import time
from typing import Optional, List
from pathlib import Path

# Import your existing utilities
from ..core.commands.builders import (
    build_arp_scan_cmd, build_nmap_arp_scan_cmd, build_ping_cmd,
    build_traceroute_cmd, build_nmap_scan_cmd, build_nmap_firewall_scan_cmd
)
from ..utils.validation import validate_ip, validate_port_range, validate_packet_size, validate_packet_count
from ..utils.logging import setup_logging, get_logger, log_scan_start, log_scan_complete
from .formatters import ScanResultFormatter
from ..utils.common import run_command_save, oper_system, clear_screen, splash_screen
from ..platforms.linux import is_sudo_linux, check_and_run_sudo_linux
from ..platforms.windows import *

# Create the main Typer app
app = typer.Typer(
    name="omni-scanner",
    help="Comprehensive network scanning tool with ARP, ping, traceroute, and nmap capabilities",
    add_completion=False
)

# Global state for logging
logger = None
formatter = None


def setup_globals(verbose: bool = False, quiet: bool = False, log_file: Optional[str] = None):
    """Set up global logger and formatter."""
    global logger, formatter
    logger = setup_logging(
        level="DEBUG" if verbose else "INFO",
        log_to_file=True,
        log_file=log_file,
        quiet=quiet,
        verbose=verbose
    )
    formatter = ScanResultFormatter()


@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress output except errors"),
    log_file: Optional[str] = typer.Option(None, "--log-file", help="Custom log file path")
):
    """Omni-Scanner: Comprehensive network scanning tool."""
    setup_globals(verbose, quiet, log_file)


@app.command()
def arp(
    target: Optional[str] = typer.Argument(None, help="Target network (CIDR notation or IP range)"),
    fast: bool = typer.Option(False, "--fast", "-f", help="Use fast scan options"),
    interface: Optional[str] = typer.Option(None, "--interface", "-i", help="Network interface to use"),
    output_format: str = typer.Option("json", "--format", help="Output format: json, csv, html"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Output file (without extension)")
):
    """Perform ARP scan to discover hosts on the network."""
    global logger, formatter
    
    logger.info("Starting ARP scan")
    
    # Use nmap ARP scan if target is specified, otherwise use arp-scan
    if target:
        if not validate_ip(target):
            typer.echo(f"Error: Invalid target '{target}'", err=True)
            raise typer.Exit(1)
        
        log_scan_start(logger, "nmap-arp", target)
        cmd = build_nmap_arp_scan_cmd(target)
    else:
        # Check for sudo on Linux
        if oper_system == 'linux' and not is_sudo_linux():
            typer.echo("Error: ARP scan requires sudo privileges on Linux", err=True)
            raise typer.Exit(1)
        
        log_scan_start(logger, "arp", "local network")
        cmd = build_arp_scan_cmd(
            target=target,
            fast=fast,
            interface=interface,
            sudo_required=True
        )
    
    # Execute scan
    start_time = time.time()
    output = run_command_save(cmd, "arp-scan")
    duration = time.time() - start_time
    
    # Format and save results
    if output_file is None:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = f"arp_scan_{timestamp}"
    
    # Parse and format output
    if target:
        data = formatter.parse_nmap_output(output)
    else:
        data = formatter.parse_arp_scan_output(output)
    
    # Export in requested format
    if output_format.lower() == "json":
        result_file = formatter.export_to_json(data, output_file)
    elif output_format.lower() == "csv":
        result_file = formatter.export_to_csv(data, output_file)
    elif output_format.lower() == "html":
        result_file = formatter.export_to_html(data, output_file)
    else:
        typer.echo(f"Error: Unsupported format '{output_format}'", err=True)
        raise typer.Exit(1)
    
    log_scan_complete(logger, "arp", target or "local network", duration, result_file)
    
    # Show summary
    summary = formatter.generate_summary(data)
    typer.echo(f"✅ {summary}")
    typer.echo(f"📄 Results saved to: {result_file}")


@app.command()
def ping(
    target: str = typer.Argument(..., help="Target IP address or hostname"),
    count: Optional[int] = typer.Option(None, "--count", "-c", help="Number of packets to send"),
    size: Optional[int] = typer.Option(None, "--size", "-s", help="Packet size in bytes"),
    timeout: Optional[float] = typer.Option(None, "--timeout", "-t", help="Timeout in seconds"),
    flood: bool = typer.Option(False, "--flood", help="Flood ping (requires sudo)"),
    infinite: bool = typer.Option(False, "--infinite", help="Ping infinitely"),
    output_format: str = typer.Option("json", "--format", help="Output format: json, csv, html"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Output file (without extension)")
):
    """Perform ping scan to test connectivity to a host."""
    global logger, formatter
    
    # Validate inputs
    if not validate_ip(target.split('/')[0]):  # Handle CIDR notation
        typer.echo(f"Error: Invalid target '{target}'", err=True)
        raise typer.Exit(1)
    
    if size and not validate_packet_size(str(size)):
        typer.echo(f"Error: Invalid packet size '{size}' (must be 0-65500)", err=True)
        raise typer.Exit(1)
    
    if count and not validate_packet_count(str(count)):
        typer.echo(f"Error: Invalid packet count '{count}' (must be positive)", err=True)
        raise typer.Exit(1)
    
    # Check for sudo if flood ping is requested
    if flood and oper_system == 'linux' and not is_sudo_linux():
        typer.echo("Error: Flood ping requires sudo privileges on Linux", err=True)
        raise typer.Exit(1)
    
    log_scan_start(logger, "ping", target, {
        "count": count, "size": size, "timeout": timeout, "flood": flood
    })
    
    # Build and execute command
    cmd = build_ping_cmd(
        target=target,
        count=count,
        packet_size=size,
        timeout=timeout,
        flood=flood,
        infinite=infinite,
        sudo_required=is_sudo_linux() if oper_system == 'linux' else False
    )
    
    start_time = time.time()
    output = run_command_save(cmd, "ping-scan")
    duration = time.time() - start_time
    
    # Format and save results
    if output_file is None:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = f"ping_scan_{timestamp}"
    
    data = formatter.parse_ping_output(output, target)
    
    # Export in requested format
    if output_format.lower() == "json":
        result_file = formatter.export_to_json(data, output_file)
    elif output_format.lower() == "csv":
        result_file = formatter.export_to_csv(data, output_file)
    elif output_format.lower() == "html":
        result_file = formatter.export_to_html(data, output_file)
    else:
        typer.echo(f"Error: Unsupported format '{output_format}'", err=True)
        raise typer.Exit(1)
    
    log_scan_complete(logger, "ping", target, duration, result_file)
    
    # Show summary
    summary = formatter.generate_summary(data)
    typer.echo(f"✅ {summary}")
    typer.echo(f"📄 Results saved to: {result_file}")


@app.command()
def traceroute(
    target: str = typer.Argument(..., help="Target IP address or hostname"),
    max_hops: Optional[int] = typer.Option(None, "--max-hops", "-m", help="Maximum number of hops"),
    timeout: Optional[float] = typer.Option(None, "--timeout", "-t", help="Timeout per hop in seconds"),
    port: Optional[int] = typer.Option(None, "--port", "-p", help="Port to use for tracing (Linux only)"),
    output_format: str = typer.Option("json", "--format", help="Output format: json, csv, html"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Output file (without extension)")
):
    """Perform traceroute to trace network path to a host."""
    global logger, formatter
    
    if not validate_ip(target.split('/')[0]):
        typer.echo(f"Error: Invalid target '{target}'", err=True)
        raise typer.Exit(1)
    
    if port and not validate_port_range(str(port)):
        typer.echo(f"Error: Invalid port '{port}'", err=True)
        raise typer.Exit(1)
    
    log_scan_start(logger, "traceroute", target, {
        "max_hops": max_hops, "timeout": timeout, "port": port
    })
    
    cmd = build_traceroute_cmd(
        target=target,
        max_hops=max_hops,
        timeout=timeout,
        port=port
    )
    
    start_time = time.time()
    output = run_command_save(cmd, "traceroute-scan")
    duration = time.time() - start_time
    
    # For now, save as raw output with basic structure
    if output_file is None:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = f"traceroute_scan_{timestamp}"
    
    data = {
        "scan_type": "traceroute",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "target": target,
        "raw_output": output
    }
    
    result_file = formatter.export_to_json(data, output_file)
    log_scan_complete(logger, "traceroute", target, duration, result_file)
    
    typer.echo(f"✅ Traceroute to {target} completed in {duration:.2f} seconds")
    typer.echo(f"📄 Results saved to: {result_file}")


@app.command()
def nmap(
    target: str = typer.Argument(..., help="Target IP address, range, or network"),
    ports: Optional[str] = typer.Option(None, "--ports", "-p", help="Port specification (e.g., 80,443 or 1-1000)"),
    top_ports: Optional[int] = typer.Option(None, "--top-ports", help="Scan top N most common ports (1-65535)"),
    scan_type: str = typer.Option("syn", "--scan-type", "-s", help="Scan type: syn, tcp, udp, ping, ack"),
    os_detect: bool = typer.Option(False, "--os-detect", "-O", help="Enable OS detection"),
    service_detect: bool = typer.Option(False, "--service-detect", "-sV", help="Enable service detection"),
    timing: str = typer.Option("T4", "--timing", "-T", help="Timing template (T0-T5: T0=slowest, T5=fastest)"),
    firewall_evasion: bool = typer.Option(False, "--firewall-evasion", "-f", help="Use firewall evasion techniques"),
    output_format: str = typer.Option("json", "--format", help="Output format: json, csv, html"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Output file (without extension)")
):
    """
    Perform Nmap scan with various options.
    
    Examples:
        omni-scanner nmap 192.168.1.1 --top-ports 100
        omni-scanner nmap 192.168.1.0/24 --ports 80,443,22 -sV
        omni-scanner nmap scanme.nmap.org --timing T1 --os-detect
    """
    global logger, formatter
    
    if not validate_ip(target):
        typer.echo(f"Error: Invalid target '{target}'", err=True)
        raise typer.Exit(1)
    
    if ports and not validate_port_range(ports):
        typer.echo(f"Error: Invalid port specification '{ports}'", err=True)
        raise typer.Exit(1)
    
    if top_ports is not None and (top_ports < 1 or top_ports > 65535):
        typer.echo(f"Error: top-ports must be between 1 and 65535", err=True)
        raise typer.Exit(1)
    
    if ports and top_ports:
        typer.echo("Warning: --top-ports takes precedence over --ports", err=True)
    
    log_scan_start(logger, "nmap", target, {
        "ports": ports, "top_ports": top_ports, "scan_type": scan_type, "timing": timing
    })
    
    start_time = time.time()
    
    if firewall_evasion:
        # Use legacy command builder for firewall evasion
        cmd = build_nmap_firewall_scan_cmd(target, ports, timing)
        output = run_command_save(cmd, "nmap-scan")
        duration = time.time() - start_time
        
        # Parse output manually for firewall evasion scans
        data = formatter.parse_nmap_output(output)
    else:
        # Use NmapScanner for better progress tracking
        from ..core.scanners.nmap_scanner import NmapScanner
        scanner = NmapScanner()
        
        # Perform scan with progress bar
        success, output, parsed_data = scanner.scan(
            target=target,
            ports=ports,
            scan_type=scan_type,
            service_detection=service_detect,
            timing=timing,
            top_ports=top_ports,
            show_progress=True
        )
        
        duration = time.time() - start_time
        
        if not success:
            typer.echo(f"❌ Nmap scan failed: {output}", err=True)
            raise typer.Exit(1)
        
        # Use parsed data from scanner
        data = parsed_data if parsed_data else formatter.parse_nmap_output(output)
    
    # Format and save results
    if output_file is None:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = f"nmap_scan_{timestamp}"
    
    # Export in requested format
    if output_format.lower() == "json":
        result_file = formatter.export_to_json(data, output_file)
    elif output_format.lower() == "csv":
        result_file = formatter.export_to_csv(data, output_file)
    elif output_format.lower() == "html":
        result_file = formatter.export_to_html(data, output_file)
    else:
        typer.echo(f"Error: Unsupported format '{output_format}'", err=True)
        raise typer.Exit(1)
    
    log_scan_complete(logger, "nmap", target, duration, result_file)
    
    # Show summary
    summary = formatter.generate_summary(data)
    typer.echo(f"✅ {summary}")
    typer.echo(f"📄 Results saved to: {result_file}")


@app.command()
def interactive():
    """Launch the interactive menu interface (original mode)."""
    typer.echo("🚀 Launching interactive mode...")
    
    # Import and run your existing menu system
    from ..platforms.linux import menu_linux
    from ..platforms.windows import menu_windows
    
    try:
        time.sleep(0.7)
        clear_screen()
        splash_screen()
        
        while True:
            if oper_system == 'windows':
                menu_windows()
            elif oper_system == 'linux':
                menu_linux()
            break
    except KeyboardInterrupt:
        pass
    finally:
        time.sleep(0.5)
        clear_screen()


@app.command()
def dns(
    target: str = typer.Argument(..., help="Hostname or IP address to lookup"),
    reverse: bool = typer.Option(False, "--reverse", "-r", help="Perform reverse DNS lookup"),
    advanced: bool = typer.Option(False, "--advanced", "-a", help="Perform advanced DNS lookup with multiple record types"),
    record_types: Optional[List[str]] = typer.Option(None, "--types", "-t", help="DNS record types for advanced lookup (A, AAAA, MX, NS, TXT, CNAME)"),
    output_format: str = typer.Option("json", "--format", "-f", help="Output format (json, csv, html)"),
    save_file: Optional[str] = typer.Option(None, "--save", "-s", help="Save results to file"),
):
    """
    Perform DNS lookup operations.
    
    Examples:
        omni-scanner dns google.com
        omni-scanner dns 8.8.8.8 --reverse
        omni-scanner dns google.com --advanced
        omni-scanner dns google.com --advanced --types A MX NS
    """
    setup_globals()
    
    from ..core.scanners.dns_scanner import DNSScanner
    
    typer.echo(f"🔍 DNS Lookup: {target}")
    typer.echo(f"Mode: {'Reverse' if reverse else 'Advanced' if advanced else 'Forward'}")
    
    dns_scanner = DNSScanner()
    
    try:
        if reverse:
            success, output, results = dns_scanner.reverse_lookup(target)
        elif advanced:
            types = record_types if record_types else ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
            success, output, results = dns_scanner.advanced_dns_lookup(target, types)
        else:
            success, output, results = dns_scanner.forward_lookup(target)
        
        if success:
            typer.echo(f"✅ {output}")
        else:
            typer.echo(f"❌ {output}")
        
        # Format and save results
        if results and formatter:
            formatted_output = formatter.format_results(results, output_format)
            
            if save_file:
                formatter.save_results(formatted_output, save_file, output_format)
                typer.echo(f"💾 Results saved to: {save_file}")
            else:
                typer.echo(formatted_output)
        
    except Exception as e:
        typer.echo(f"❌ DNS lookup failed: {e}")
        raise typer.Exit(1)


@app.command()
def bulk_dns(
    targets_file: str = typer.Argument(..., help="File containing hostnames/IPs (one per line)"),
    output_format: str = typer.Option("json", "--format", "-f", help="Output format (json, csv, html)"),
    save_file: Optional[str] = typer.Option(None, "--save", "-s", help="Save results to file"),
):
    """
    Perform bulk DNS lookups from a file.
    
    Example:
        omni-scanner bulk-dns targets.txt --save dns_results.json
    """
    setup_globals()
    
    from ..core.scanners.dns_scanner import DNSScanner
    
    try:
        # Read targets from file
        with open(targets_file, 'r') as f:
            targets = [line.strip() for line in f.readlines() if line.strip()]
        
        if not targets:
            typer.echo(f"❌ No targets found in {targets_file}")
            raise typer.Exit(1)
        
        typer.echo(f"🔍 Bulk DNS Lookup: {len(targets)} targets")
        
        dns_scanner = DNSScanner()
        success, output, results = dns_scanner.bulk_dns_lookup(targets)
        
        typer.echo(f"✅ {output}")
        
        # Format and save results
        if results and formatter:
            formatted_output = formatter.format_results(results, output_format)
            
            if save_file:
                formatter.save_results(formatted_output, save_file, output_format)
                typer.echo(f"💾 Results saved to: {save_file}")
            else:
                typer.echo(formatted_output)
        
    except FileNotFoundError:
        typer.echo(f"❌ File not found: {targets_file}")
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Bulk DNS lookup failed: {e}")
        raise typer.Exit(1)


@app.command(name="system-deps")
def system_deps(
    check: bool = typer.Option(False, "--check", help="Check dependency status"),
    install: bool = typer.Option(False, "--install", help="Install missing dependencies"),
    auto: bool = typer.Option(False, "--auto", help="Auto-install without confirmation"),
    instructions: bool = typer.Option(False, "--instructions", help="Show installation instructions")
):
    """
    Check and install system dependencies (nmap, arp-scan, traceroute).
    
    Examples:
        omni-scanner system-deps --check
        omni-scanner system-deps --install
        omni-scanner system-deps --instructions
    """
    from ..utils.system_deps import SystemDependencyInstaller
    
    installer = SystemDependencyInstaller()
    
    if instructions:
        typer.echo(installer.get_installation_instructions())
        return
    
    if check or not any([install, instructions]):
        typer.echo("🔍 Checking system dependencies...")
        status = installer.check_all_dependencies()
        
        missing = [tool for tool, available in status.items() if not available]
        if missing:
            typer.echo(f"\n❌ Missing dependencies: {', '.join(missing)}")
            typer.echo("\nRun 'omni-scanner system-deps --install' to install missing dependencies")
            typer.echo("Or use 'omni-scanner system-deps --instructions' for manual installation steps")
        else:
            typer.echo("\n✅ All dependencies are installed!")
    
    if install:
        installer.install_missing_dependencies(auto_install=auto)


@app.command()
def version():
    """Show version information."""
    typer.echo("Omni-Scanner v1.0.0")
    typer.echo("Comprehensive network scanning tool")
    typer.echo("Created by Kartik")


if __name__ == "__main__":
    app()