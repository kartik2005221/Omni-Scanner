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

Omni-Scanner is a professional network analysis suite designed for comprehensive reconnaissance, diagnostics, and security auditing. Below is the complete documentation for v1.0's functionality:

1. Scanning Full Network (Find Specific Host)
    Advanced network discovery with multiple scanning methodologies like Arp-Scan and NMap Scan.
    - How It Works:
        ARP Scan (High Speed): Utilizes Address Resolution Protocol for lightning-fast detection of all active devices on the local network segment. This method is optimized for efficiency with minimal network overhead. (sudo required) (Linux only)
        Nmap-Based Scan: Implements intelligent target selection with customizable IP ranges, providing detailed port mapping and service detection.
    - Features:
        Automatic subnet detection for simplified scanning in ARP Scan mode
    - When to Use:
        ARP for immediate network inventory
        Nmap for targeted security assessments or when in windows

2. Ping Custom IP (Enhanced)
    Advanced ICMP diagnostics with professional customization.
    - How It Works:
        Standard Ping: ICMP echo requests with configurable packet size, interval, and timeout.
        Flood Ping Mode: High-velocity packet transmission (100+ pings/sec) for network stress testing (requires sudo).
        and more available.
    - When to Use:
        Baseline connectivity testing
        MTU path discovery
        Network resilience testing (ethical use only)

3. Trace Routing
    Comprehensive path analysis with next-gen features.
    - How It Works:
        Hybrid TTL-based tracing using ICMP/UDP/TCP protocols
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
        and more available.
    - When to Use:
        Penetration testing engagements
        Critical server audits
        Compliance verification

5. Advanced Scanning (Range of IPs)
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
        Device brand classification
    - When to Use:
        Identifying unknown network devices
        Security incident investigations
        Network documentation

7. Show Network Info
    Comprehensive local network information.
    - How It Works:
        Displays:
        - All active network interfaces
        - IP addresses and netmasks
        - Default gateways
        - DNS configurations
        and more of current device.
    - When to Use:
        Quick network status checks
        Troubleshooting connectivity issues
        System configuration verification

[S] Switch to SUDO Mode
    Switching to Full Functionality Mode (Linux Only)
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
        Speed: Completes in seconds (covers 254 IPs in under 3 seconds approx).
        Requirements:
            - Full Functionality Mode (raw packet crafting).
            - Local network access (does not work across subnets).
    When to Use:
        - Quickly audit connected devices (e.g., home/office networks).
        - Identify unauthorized devices (e.g., intruders on a Wi-Fi network).
    Availability: Linux only with Full Functionality mode.
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
-----------------|-------------------|------------------------|------------------------
Method           | ARP               | ICMP Ping              | Nmap
Speed            | Instant           | Fast                   | Slow to Moderate
Detail Level     | Basic (IP+MAC)    | Basic (Online Status)  | Advanced (Ports,Services,OS)
Network Scope    | Local Subnet Only | Any Reachable IP       | Any Reachable IP/Subnet
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
    When to Use:
        - Confirm if a device is online (router, server, etc.)
        - Measure average latency (round-trip time)

[2] Extended Ping
    Purpose: Test network performance with customizable packets.
    Technical Details:
        Method: Sends ICMP packets with user-defined sizes
        Customization: 
            - Packet size: Up to 65,500 bytes (maximum possible)
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
        Default Duration: 5 seconds
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
    Requirements:
        traceroute must be installed (Linux).
        No elevated privileges needed unless restricted by system policy.

[2] Firewall-Evasion Traceroute (TCP port 80) (sudo required)(linux only)
    Description: Performs a traceroute using TCP SYN packets to port 80 (HTTP). Linux-only.
    How It Works:
        Sends TCP SYN packets to port 80 (HTTP).
        Mimics web traffic to bypass firewalls blocking ping/UDP.
    Use Case:
        Tracing routes through firewalled networks.
        Penetration testing scenarios.
    Requirements: 
        Requires sudo privileges.
        Linux systems only.

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

Advanced Scan Menu - The Advanced Scan menu offers powerful network reconnaissance tools to analyze targets in depth. Choose between single IP or IP range scanning, then select from various techniques to suit your needs.

Scan Types:
    [4] Advanced scan (single IP) - Scan one specific target
    [5] Advanced scan (IP range) - Scan multiple targets in a range

Scan Options (appear after selecting 4 or 5):
    [1] Simple Nmap scan (fast)
        Purpose: Quickly check for open ports on a target
        Best For: Initial reconnaissance
        Note: Use alone, not combinable with other options

    [2] Detect operating system
        Purpose: Identify target's OS (Windows, Linux, etc.)
        Method: Network response fingerprinting

    [3] Detect running services and versions
        Purpose: Find software versions on open ports
        Best For: Vulnerability identification

    [4] SYN scan
        Purpose: Stealthy port discovery
        Advantage: Avoids full TCP connection logging

    [5] UDP scan
        Purpose: Find open UDP ports
        Critical For: DNS, DHCP, and VoIP services

    [6] Specific port scan
        Purpose: Focus on user-defined ports
        Usage: Enter ports like "80,443,22" when prompted

    [7] Full port scan
        Purpose: Comprehensive 65,535 port check
        Warning: Time-consuming - use judiciously

    [8] Aggressive scan
        Includes: OS detection, service versions, script scanning
        Best For: Professional security audits

    [9] Firewall bypass scan
        Purpose: Evade basic firewall protections
        Method: Uses fragmented packets and other techniques

   [10] Disable ARP ping
        Purpose: Avoid detection by local routers
        Useful For: Internal network stealth scanning

Utility Options:
    [P] Show top 50 common ports - Quick reference
    [H] Help - Display this information
    [0] Back - Return to main menu

Key Rules:
    1. Combination Rules:
       - Can combine most options (e.g., "2 3 4" for OS, services, and SYN scan)
       - Never combine 6 and 7 (specific vs full port scan)
       - Option 1 (Simple Nmap) must be used alone
    
    2. Performance Considerations:
       - UDP scans (5) are slower than TCP scans
       - Aggressive scans (8) generate significant traffic
       - Firewall bypass (9) increases scan duration
    
    3. Ethical Guidelines:
       - Always obtain proper authorization
       - Avoid scanning during business-critical hours
       - Consider using stealth options on production networks

Sample Use Cases:
• Quick Check: Option 1 (Simple Nmap)
• Security Audit: "2 3 8" (OS, services, aggressive)
• Network Troubleshooting: "5" (UDP scan for DNS issues)
• Stealth Assessment: "4 10" (SYN scan with ARP disable)

Warnings:
     Unauthorized scanning may violate computer crime laws
     Aggressive scans may trigger intrusion detection systems
     Scanning critical systems may cause service disruptions

© AiR {Kartik} 2025 | Licensed for Ethical Use Only
"""

ports = r"""
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

Top 50 Common Network Ports
    [1] 80/TCP       - HTTP (Web traffic)  
    [2] 443/TCP      - HTTPS (Secure web traffic)  
    [3] 22/TCP       - SSH (Secure Shell)  
    [4] 53/TCP/UDP   - DNS (Domain Name System)  
    [5] 25/TCP       - SMTP (Email delivery)  
    [6] 110/TCP      - POP3 (Email retrieval)  
    [7] 143/TCP      - IMAP (Email management)  
    [8] 21/TCP       - FTP Control (File Transfer Protocol)  
    [9] 23/TCP       - Telnet (Unencrypted remote access)  
   [10] 3389/TCP     - RDP (Remote Desktop Protocol)  
   [11] 445/TCP      - SMB (Windows file/printer sharing)  
   [12] 139/TCP      - NetBIOS Session Service  
   [13] 137/UDP      - NetBIOS Name Service  
   [14] 138/UDP      - NetBIOS Datagram Service  
   [15] 3306/TCP     - MySQL Database  
   [16] 5432/TCP     - PostgreSQL Database  
   [17] 587/TCP      - SMTP Submission (Secure email sending)  
   [18] 993/TCP      - IMAPS (IMAP over SSL)  
   [19] 995/TCP      - POP3S (POP3 over SSL)  
   [20] 161/UDP      - SNMP (Network monitoring)  
   [21] 162/UDP      - SNMP Trap (SNMP alerts)  
   [22] 123/UDP      - NTP (Network Time Protocol)  
   [23] 514/UDP      - Syslog (Logging service)  
   [24] 67/UDP       - DHCP Server (IP assignment)  
   [25] 68/UDP       - DHCP Client  
   [26] 389/TCP/UDP  - LDAP (Directory services)  
   [27] 636/TCP      - LDAPS (LDAP over SSL)  
   [28] 8443/TCP     - HTTPS Alternate (Common for web apps)  
   [29] 8080/TCP     - HTTP Alternate (Proxy/web caching)  
   [30] 27017/TCP    - MongoDB Database  
   [31] 6379/TCP     - Redis (In-memory database)  
   [32] 11211/TCP/UDP- Memcached (Caching system)  
   [33] 1194/UDP     - OpenVPN  
   [34] 500/UDP      - IKE (IPsec key exchange)  
   [35] 4500/UDP     - IPsec NAT-Traversal  
   [36] 1433/TCP     - Microsoft SQL Server  
   [37] 1521/TCP     - Oracle Database  
   [38] 2049/TCP/UDP - NFS (Network File System)  
   [39] 873/TCP      - Rsync (File synchronization)  
   [40] 5060/TCP/UDP - SIP (VoIP signaling)  
   [41] 5061/TCP     - SIP-TLS (Secure SIP)  
   [42] 5900/TCP     - VNC (Remote desktop)  
   [43] 25565/TCP    - Minecraft Server  
   [44] 3128/TCP     - Squid Proxy  
   [45] 69/UDP       - TFTP (Trivial File Transfer Protocol)  
   [46] 2222/TCP     - SSH Alternate (Custom deployments)  
   [47] 9200/TCP     - Elasticsearch (Search engine)  
   [48] 9300/TCP     - Elasticsearch Cluster Communication  
   [49] 5601/TCP     - Kibana (Data visualization for Elasticsearch)  
   [50] 2483/TCP     - Oracle Database SSL 

Key Notes
    - TCP vs. UDP: Some services use both (e.g., DNS, LDAP), while others are UDP-only (e.g., DHCP, SNMP, NTP).  
    - Legacy Protocols: Ports like Telnet (23) and FTP (21) are insecure and often replaced by SSH (22) and SFTP/SCP.  
    - Security: Ports like 443 (HTTPS), 993 (IMAPS), and 995 (POP3S) encrypt traffic by default.  
    - Dynamic/Ephemeral Ports: Client-side ports (e.g., 49152–65535) are temporary and not listed here.  

Warnings
    Ethical Use: Always obtain permission before scanning. Unauthorized scans may be illegal.

[0] Back

© AiR {Kartik} 2025 | Licensed for Ethical Use Only
"""

if __name__ == "__main__":
    # This file is not meant to be run directly
    # It should be imported and used in main.py
    # If this file is run directly, it will print an error message
    print("Wrong file selected for running\nPlease run 'main.py' file by using 'python main.py' command")
