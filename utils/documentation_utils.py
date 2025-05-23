help0 = r"""
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║   ░█▀█░█▄█░█▀█░▀█▀░░░░░█▀▀░█▀▀░█▀█░█▀█░█▀█░█▀▀░█▀▄    ║
║   ░█░█░█░█░█░█░░█░░▄▄▄░▀▀█░█░░░█▀█░█░█░█░█░█▀▀░█▀▄    ║
║   ░▀▀▀░▀░▀░▀░▀░▀▀▀░░░░░▀▀▀░▀▀▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀░▀    ║
║                                                       ║
║                 Omni-Scanner v1.0                     ║
║                Crafted by AiR ©2025                   ║
║        An All-in-One Network Scanning Tool            ║
║                                                       ║
╚═════════════════════════════════════[Ethical Use Only]╝

Omni-Scanner v1.0 Documentation
    Ethical and Legal Use Only
    Brand is not responsible for any illegal use

Omni-Scanner is a professional network analysis suite designed for comprehensive reconnaissance, diagnostics, and security auditing. Below is the complete documentation for v1.0's enhanced functionality:

1. Scanning Full Network (Find Specific Host)
    Advanced network discovery with multiple scanning methodologies.
    - How It Works:
        ARP Scan (High Speed): Utilizes Address Resolution Protocol for lightning-fast detection of all active devices on the local network segment. This method is optimized for efficiency with minimal network overhead. (sudo required) (Linux/macOS only)
        Nmap-Based Scan: Implements intelligent target selection with customizable IP ranges, providing detailed port mapping and service detection.
    - New Features:
        Automatic subnet detection for simplified scanning
        Interactive host selection post-discovery
        Exportable results in multiple formats
    - When to Use:
        ARP for immediate network inventory
        Nmap for targeted security assessments

2. Ping Custom IP (Enhanced)
    Advanced ICMP diagnostics with professional customization.
    - How It Works:
        Standard Ping: ICMP echo requests with configurable packet size, interval, and timeout.
        Flood Ping Mode: High-velocity packet transmission (100+ pings/sec) for network stress testing (requires sudo).
        New: Jitter calculation and packet loss statistics
    - When to Use:
        Baseline connectivity testing
        MTU path discovery
        Network resilience testing (ethical use only)

3. Trace Routing (Professional Edition)
    Comprehensive path analysis with next-gen features.
    - How It Works:
        Hybrid TTL-based tracing using ICMP/UDP/TCP protocols
        New: GeoIP lookup for each hop (when available)
        ASN (Autonomous System Number) identification
        Latency profiling at each network segment
    - When to Use:
        Diagnosing international routing issues
        Identifying peering point bottlenecks
        Network topology mapping

4. Advanced Scanning (Single IP)
    Enterprise-grade single target analysis.
    - How It Works:
        Nmap-powered scanning suite with:
        - SYN Stealth Scan (-sS)
        - Full TCP Connect Scan (-sT)
        - Version Detection (-sV)
        - OS Fingerprinting (-O)
        New: Vulnerability probability assessment
    - When to Use:
        Penetration testing engagements
        Critical server audits
        Compliance verification

5. Advanced Scanning (IP Range)
    Large-scale network reconnaissance.
    - How It Works:
        Parallelized Nmap scanning with:
        - Customizable concurrency controls
        - Intelligent host grouping
        - Adaptive timing profiles
        New: CIDR notation support (/24, /16 etc.)
    - When to Use:
        Enterprise network audits
        Data center inventories
        Security posture assessments

6. MAC Vendor Lookup (Online)
    Enhanced device identification.
    - How It Works:
        Real-time OUI (Organizationally Unique Identifier) database queries
        Local cache for offline lookups
        New: Device type classification
    - When to Use:
        Identifying unknown network devices
        Security incident investigations
        Network documentation

7. Show Network Info
    Comprehensive local network intelligence.
    - How It Works:
        Displays:
        - All active network interfaces
        - IP addresses and netmasks
        - Default gateways
        - DNS configurations
        New: Bandwidth usage monitoring
    - When to Use:
        Quick network status checks
        Troubleshooting connectivity issues
        System configuration verification

[S] Switch to SUDO Mode
    Dynamic privilege escalation.
    - How It Works:
        Seamless transition between user and root privileges
        Maintains session state during escalation
        New: Privilege verification system
    - When to Use:
        When ARP or flood ping features are needed
        For advanced Nmap scanning options

Additional Commands
    [H] Help: Displays this documentation
    [0] Quit: Safely terminates the program

Important Notes
    - Ethical Compliance:
        All scanning activities must comply with local laws and regulations.
        Written authorization is required for scanning third-party networks.
        Flood testing requires explicit network owner consent.
    - Performance Optimization:
        Use ARP scans for local network discovery (fastest method)
        Adjust thread count in settings for large IP ranges
        Consider network bandwidth during intensive operations
    - System Requirements:
        Python 3.8+ with required dependencies
        Nmap 7.80+ for advanced features
        Root privileges for certain operations
        Internet access for MAC vendor lookups

© AiR {Kartik} 2025 | Licensed for Ethical Use Only
"""

help1 = r"""
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║   ░█▀█░█▄█░█▀█░▀█▀░░░░░█▀▀░█▀▀░█▀█░█▀█░█▀█░█▀▀░█▀▄    ║
║   ░█░█░█░█░█░█░░█░░▄▄▄░▀▀█░█░░░█▀█░█░█░█░█░█▀▀░█▀▄    ║
║   ░▀▀▀░▀░▀░▀░▀░▀▀▀░░░░░▀▀▀░▀▀▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀░▀    ║
║                                                       ║
║                 Omni-Scanner v1.0                     ║
║                Crafted by AiR ©2025                   ║
║        An All-in-One Network Scanning Tool            ║
║                                                       ║
╚═════════════════════════════════════[Ethical Use Only]╝

Omni-Scanner v1.0 Documentation
    Ethical and Legal Use Only
    Brand is not responsible for any illegal use

Arp Menu - This menu provides three methods to identify and analyze devices on your network.

1. Fast Scan: All IPs on Network (Less Detailed)
    Purpose: Rapidly discover all active devices on the local network.
    Technical Details:
        Method: ARP (Address Resolution Protocol) scanning.
        How It Works:
            - Broadcasts ARP requests across the network.
            - Lists devices that respond with their IP and MAC addresses.
        Speed: Completes in seconds (covers 254 IPs in under 3 seconds).
        Requirements:
            - sudo/administrator privileges (raw packet crafting).
            - Local network access (does not work across subnets).
    When to Use:
        - Quickly audit connected devices (e.g., home/office networks).
        - Identify unauthorized devices (e.g., intruders on a Wi-Fi network).
    Availability: Linux only with sudo privileges.
    Limitations:
        - No port or service details.
        - Limited to the local subnet.

2. Fast Scan: Specific IP(s) (Less Detailed)
    Purpose: Quickly check the status of specific IP addresses.
    Technical Details:
        Method: ICMP ping sweep.
        How It Works:
            - Sends ICMP echo requests to specified IPs.
            - Identifies responsive hosts.
        Speed: Faster than Nmap-based scans.
    When to Use:
        - Verify if specific hosts are online.
        - Quick connectivity checks.
    Limitations:
        - Less detailed than Nmap scans.
        - May be blocked by firewalls.

3. Deep Scan: Specific IP(s) (More Detailed, Slower)
    Purpose: Perform an in-depth analysis of specific IPs or ranges.
    Technical Details:
        Method: Nmap-based scanning.
        How It Works:
            - Uses nmap <IP range> to probe ports, services, and host behavior.
            - Can detect:
                - Open/closed ports.
                - Running services (e.g., HTTP, SSH).
                - Operating system fingerprints.
        Speed: Slower due to comprehensive checks (seconds to minutes).
    When to Use:
        - Security audits of critical devices (e.g., servers, routers).
        - Troubleshooting connectivity or service issues.
    Example Commands:
        - nmap 192.168.1.1-50 → Scans IPs 1 to 50.
        - nmap 192.168.1.10 → Scans a single IP.

Key Differences -
Feature          | Fast Scan All IPs | Fast Scan Specific IPs | Deep Scan Specific IPs
----------------|-------------------|------------------------|------------------------
Method           | ARP               | ICMP Ping              | Nmap
Speed            | Instant           | Fast                   | Slow to Moderate
Detail Level     | Basic (IP+MAC)    | Basic (Online Status)   | Advanced (Ports,Services,OS)
Network Scope    | Local Subnet Only | Any Reachable IP        | Any Reachable IP/Subnet
Privileges       | Requires sudo     | Optional               | Optional (depends on scan type)

Important Notes
    Ethical Use:
        - Always obtain explicit permission before scanning. Unauthorized scanning may violate privacy laws.
        - ARP and ICMP scans are less intrusive. Nmap scans may trigger security alerts.
    
    Performance Tips:
        - For ARP scans, avoid overlapping with other network-heavy tasks.
        - For Nmap, narrow IP ranges to reduce scan time (e.g., 192.168.1.1-20).
    
    Dependencies:
        - ARP Scan: Requires scapy Python library.
        - Nmap Scan: Requires nmap installed on the system.
        - ICMP Scan: Requires standard networking tools.

Navigation:
    [H] Help        [0] Back to Main Menu

© AiR {Kartik} 2025 | Licensed for Ethical Use Only
"""

help2 = r"""
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║   ░█▀█░█▄█░█▀█░▀█▀░░░░░█▀▀░█▀▀░█▀█░█▀█░█▀█░█▀▀░█▀▄    ║
║   ░█░█░█░█░█░█░░█░░▄▄▄░▀▀█░█░░░█▀█░█░█░█░█░█▀▀░█▀▄    ║
║   ░▀▀▀░▀░▀░▀░▀░▀▀▀░░░░░▀▀▀░▀▀▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀░▀    ║
║                                                       ║
║                 Omni-Scanner v1.0                     ║
║                Crafted by AiR ©2025                   ║
║        An All-in-One Network Scanning Tool            ║
║                                                       ║
╚═════════════════════════════════════[Ethical Use Only]╝

Omni-Scanner v1.0 Documentation
    Ethical and Legal Use Only
    Brand is not responsible for any illegal use

Ping Menu - This menu allows advanced customization of ICMP (Internet Control Message Protocol) ping requests to diagnose connectivity, test network performance, or simulate stress conditions.

[1] Simple Ping
    Purpose: Basic connectivity check to verify if a target IP is reachable.
    Technical Details:
        Method: Standard ICMP echo request/reply.
        Default Settings:
            - Packet Size: 56 bytes (64 bytes with headers)
            - Timeout: 2 seconds per reply
            - Number of Requests: 7 (automatic stop)
    When to Use:
        - Confirm if a device is online (router, server, etc.)
        - Measure average latency (round-trip time)

[2] Extended Ping
    Purpose: Test network performance with customizable packets.
    Technical Details:
        Method: Sends ICMP packets with user-defined sizes
        Customization: 
            - Packet size: Up to 65,500 bytes (maximum possible)
            - Number of Requests: Infinite or custom count
    Use Case:
        - Diagnose packet fragmentation issues
        - Test maximum transmission unit (MTU) compatibility
    Note: Large packets may be dropped by routers/firewalls

[3] Slow-Network Ping
    Purpose: Adjust settings for high-latency networks.
    Technical Details:
        Method: Increases wait time for ICMP replies
        Customization:
            - Timeout: Configurable (1-30 seconds)
            - Packet size: Adjustable for bandwidth testing
    Use Case:
        - Diagnose satellite/WAN links with high latency
        - Test unstable connections (mobile networks, etc.)

[4] Flood Ping (sudo required)(linux only)
    Purpose: Stress-test a target with high-speed ICMP packets.
    Technical Details:
        Method: Sends packets as fast as possible (DoS simulation)
        Requirements:
            - sudo/root privileges
            - Linux systems only
        Default Duration: 5 seconds (auto-stop)
    Use Case:
        - Test network/server resilience under heavy load
        - Bandwidth capacity testing
    Warnings:
        - May trigger security systems or cause network disruption
        - Requires explicit authorization before use

Key Notes
    Ethical Use:
        - Flood Ping is a high-risk feature requiring written consent
        - Never target unauthorized systems or critical infrastructure
    Performance Tips:
        - For MTU testing, start with 1500 byte packets
        - Limit flood pings to 5 seconds maximum
    Dependencies:
        - Requires system ping utility
        - Flood Ping requires Linux environment

Navigation:
    [H] Help        [0] Back to Main Menu

© AiR {Kartik} 2025 | Licensed for Ethical Use Only
"""
help3 = r"""
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║   ░█▀█░█▄█░█▀█░▀█▀░░░░░█▀▀░█▀▀░█▀█░█▀█░█▀█░█▀▀░█▀▄    ║
║   ░█░█░█░█░█░█░░█░░▄▄▄░▀▀█░█░░░█▀█░█░█░█░█░█▀▀░█▀▄    ║
║   ░▀▀▀░▀░▀░▀░▀░▀▀▀░░░░░▀▀▀░▀▀▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀░▀    ║
║                                                       ║
║                 Omni-Scanner v1.0                     ║
║                Crafted by AiR ©2025                   ║
║        An All-in-One Network Scanning Tool            ║
║                                                       ║
╚═════════════════════════════════════[Ethical Use Only]╝

Omni-Scanner v1.0 Documentation
    Ethical and Legal Use Only
    Brand is not responsible for any illegal use

Traceroute menu - This menu allows you to track any IP address or domain name to find the path of packets from your system to the target host.

[1] Standard Traceroute (ICMP/UDP)
    Description: Performs a traditional traceroute using ICMP (Windows) or UDP (Linux/macOS) packets to map the route from your machine to the target host.
    How It Works: 
        Linux/macOS: Uses traceroute command which sends UDP packets with increasing TTL values.
        Windows: Uses tracert command that sends ICMP Echo Requests.
    Use Case:
        General-purpose path tracing.
        Diagnosing routing issues or high-latency links.
    Commands Used:
        Linux/macOS:
            traceroute <target>
        Windows:
            tracert <target>
    Requirements:
        traceroute must be installed (Linux).
        No elevated privileges needed unless restricted by system policy.

[2] Firewall-Evasion Traceroute (TCP port 80) (sudo required)(linux only)
    Description: Performs a traceroute using TCP SYN packets to port 80 (HTTP). Linux-only in current version.
    How It Works:
        Sends TCP SYN packets to port 80 (HTTP).
        Mimics web traffic to bypass firewalls blocking ping/UDP.
    Use Case:
        Tracing routes through firewalled networks.
        Penetration testing scenarios.
    Commands Used:
        Linux/macOS:
            sudo traceroute -T -p 80 <target>
    Requirements: 
        Requires sudo privileges.
        Linux systems only in current version.

[H] Help        [0] Back

Notes:
1. For most networks, Option 1 is sufficient and faster.
2. If Option 1 fails, try Option 2 (Linux only).
3. Always run with necessary privileges for accurate results.

Warnings:
• Ethical Use: Always obtain proper authorization before scanning.
• Unauthorized scanning may violate laws and network policies.

© AiR {Kartik} 2025 | Licensed for Ethical Use Only
"""
help4 = r"""
Advanced Scan Overview
The Advanced Scan menu offers powerful network reconnaissance tools to analyze targets in depth. Each option focuses on different aspects of network exploration, from detecting open ports to identifying software vulnerabilities. Below is a breakdown of what each scan does, how it works, and when to use it.

Scan Options
    1. Simple Nmap (Fast)
        Purpose: Quickly check for open ports on a target.
        How It Works: Scans the 1,000 most common ports used by services like web servers, email, and file sharing.
        Best For: A rapid overview of a target’s active services.
        Output: Lists open ports (e.g., Port 80: HTTP - Open).
    
    2. Detect OS
        Purpose: Guess the target’s operating system (e.g., Windows, Linux).
        How It Works: Analyzes subtle differences in how devices respond to network requests to fingerprint the OS.
        Best For: Tailoring further attacks or troubleshooting compatibility issues.
        Output: Displays OS name and confidence level (e.g., Likely: Linux 4.x).
    
    3. Detect Running Service & Version
        Purpose: Identify software running on open ports (e.g., Apache 2.4.49).
        How It Works: Sends probes to open ports and analyzes responses to determine service details.
        Best For: Finding outdated or vulnerable software.
        Output: Lists service names and versions (e.g., Port 22: OpenSSH 8.2p1).
    
    4. SYN Scan (Stealth)
        Purpose: Discover open ports without fully connecting to the target.
        How It Works: Sends partial connection requests to avoid logging.
        Best For: Avoiding detection by basic firewalls or intrusion systems.
        Output: Lists open ports marked as "stealth" (e.g., Port 443: HTTPS - Stealth Open).
    
    5. UDP Scan
        Purpose: Find open UDP ports (used by DNS, VoIP, and gaming services).
        How It Works: Sends lightweight UDP packets to check for responses.
        Best For: Discovering services that don’t use TCP (e.g., DHCP servers).
        Output: Lists open UDP ports (e.g., Port 53: DNS - Open).
    
    6. Specific Port Scan
        Purpose: Scan user-defined ports (e.g., 80, 443, 22).
        How It Works: Focuses only on the ports you specify, ignoring others.
        Best For: Targeting critical services (e.g., checking if SSH or HTTP is exposed).
        Output: Detailed results for selected ports only.
    
    7. All Port Scan
        Purpose: Check all 65,535 ports on a target.
        How It Works: Systematically tests every possible port.
        Best For: Comprehensive security audits or finding hidden services.
        Output: Full list of open ports (warning: this can be very long!).
    
    8. Aggressive Scan (Slower)
        Purpose: Combine multiple advanced techniques for a deep dive.
        What’s Included:
            OS Detection (Option 2).
            Service Version Detection (Option 3).
            Script Scanning: Runs vulnerability-checking scripts.
        Port Scanning: Checks common and suspicious ports.
        Best For: Full-scale security assessments or penetration testing.
        Output: Detailed report covering OS, services, scripts, and open ports.

Key Rules
    Combining Options:
        You can select multiple scans (e.g., 2 3 4 for OS, service versions, and stealth scan).
        Do NOT select both 6 (Specific Ports) and 7 (All Ports)—they conflict!
    Use Cases:
        Simple Nmap: Quick check for home networks.
        Aggressive Scan: Professional security audits.
        UDP Scan: Diagnosing DNS or gaming server issues.
    What to Expect:
        Faster scans (e.g., Simple Nmap) provide less detail.
        Slower scans (e.g., Aggressive Scan) reveal hidden risks.

Warnings
    Ethical Use: Always obtain permission before scanning. Unauthorized scans may be illegal.
    Performance Impact: Aggressive scans may slow down your network or trigger alarms.
    Stealth Scans: While harder to detect, they are not invisible to advanced security systems.

To Return to the Main Menu, press 0.
For this Help Screen, press H.

© Kartik | Licensed for Ethical Use Only
"""

ports = r"""
Top 50 Common Network Ports
    1. 80/TCP        - HTTP (Web traffic)  
    2. 443/TCP       - HTTPS (Secure web traffic)  
    3. 22/TCP        - SSH (Secure Shell)  
    4. 53/TCP/UDP    - DNS (Domain Name System)  
    5. 25/TCP        - SMTP (Email delivery)  
    6. 110/TCP       - POP3 (Email retrieval)  
    7. 143/TCP       - IMAP (Email management)  
    8. 21/TCP        - FTP Control (File Transfer Protocol)  
    9. 23/TCP        - Telnet (Unencrypted remote access)  
    10. 3389/TCP     - RDP (Remote Desktop Protocol)  
    11. 445/TCP      - SMB (Windows file/printer sharing)  
    12. 139/TCP      - NetBIOS Session Service  
    13. 137/UDP      - NetBIOS Name Service  
    14. 138/UDP      - NetBIOS Datagram Service  
    15. 3306/TCP     - MySQL Database  
    16. 5432/TCP     - PostgreSQL Database  
    17. 587/TCP      - SMTP Submission (Secure email sending)  
    18. 993/TCP      - IMAPS (IMAP over SSL)  
    19. 995/TCP      - POP3S (POP3 over SSL)  
    20. 161/UDP      - SNMP (Network monitoring)  
    21. 162/UDP      - SNMP Trap (SNMP alerts)  
    22. 123/UDP      - NTP (Network Time Protocol)  
    23. 514/UDP      - Syslog (Logging service)  
    24. 67/UDP       - DHCP Server (IP assignment)  
    25. 68/UDP       - DHCP Client  
    26. 389/TCP/UDP  - LDAP (Directory services)  
    27. 636/TCP      - LDAPS (LDAP over SSL)  
    28. 8443/TCP     - HTTPS Alternate (Common for web apps)  
    29. 8080/TCP     - HTTP Alternate (Proxy/web caching)  
    30. 27017/TCP    - MongoDB Database  
    31. 6379/TCP     - Redis (In-memory database)  
    32. 11211/TCP/UDP- Memcached (Caching system)  
    33. 1194/UDP     - OpenVPN  
    34. 500/UDP      - IKE (IPsec key exchange)  
    35. 4500/UDP     - IPsec NAT-Traversal  
    36. 1433/TCP     - Microsoft SQL Server  
    37. 1521/TCP     - Oracle Database  
    38. 2049/TCP/UDP - NFS (Network File System)  
    39. 873/TCP      - Rsync (File synchronization)  
    40. 5060/TCP/UDP - SIP (VoIP signaling)  
    41. 5061/TCP     - SIP-TLS (Secure SIP)  
    42. 5900/TCP     - VNC (Remote desktop)  
    43. 25565/TCP    - Minecraft Server  
    44. 3128/TCP     - Squid Proxy  
    45. 69/UDP       - TFTP (Trivial File Transfer Protocol)  
    46. 2222/TCP     - SSH Alternate (Custom deployments)  
    47. 9200/TCP     - Elasticsearch (Search engine)  
    48. 9300/TCP     - Elasticsearch Cluster Communication  
    49. 5601/TCP     - Kibana (Data visualization for Elasticsearch)  
    50. 2483/TCP     - Oracle Database SSL 

Key Notes
    - TCP vs. UDP: Some services use both (e.g., DNS, LDAP), while others are UDP-only (e.g., DHCP, SNMP, NTP).  
    - Legacy Protocols: Ports like Telnet (23) and FTP (21) are insecure and often replaced by SSH (22) and SFTP/SCP.  
    - Security: Ports like 443 (HTTPS), 993 (IMAPS), and 995 (POP3S) encrypt traffic by default.  
    - Dynamic/Ephemeral Ports: Client-side ports (e.g., 49152–65535) are temporary and not listed here.  

Warnings
    Ethical Use: Always obtain permission before scanning. Unauthorized scans may be illegal.

To Return to the Main Menu, press 0.
For this Help Screen, press H.

© Kartik | Licensed for Ethical Use Only
"""

if __name__ == "__main__":
    # This file is not meant to be run directly
    # It should be imported and used in main.py
    # If this file is run directly, it will print an error message
    print("Wrong file selected for running\nPlease run 'main.py' file by using 'python main.py' command")
