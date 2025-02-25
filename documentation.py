help0 = r"""
Omni-Scanner Documentation (Help Menu)
    Ethical and Legal Use Only
    Author is not responsible for any illegal use

Omni-Scanner is a comprehensive network analysis tool designed for reconnaissance, diagnostics, and security auditing. Below is a detailed explanation of the core functionalities available in the main menu:

1. Scanning Full Network, Finding Specific Target
    This option allows you to discover active devices and analyze targets within your network.
    - How It Works:
        Scan All IPs (High Speed): Uses ARP (Address Resolution Protocol) to rapidly identify all devices connected to the local network. ARP scanning is lightweight and efficient, making it ideal for quick network inventories.
        Scan Specific IPs (Detailed): Leverages Nmap, a industry-standard tool, to perform deep scans on user-specified IP ranges. This method provides detailed insights into open ports, services, and device configurations.
    - When to Use:
        ARP scanning is best for immediate device discovery (e.g., identifying unknown devices on a home network).
        Nmap-based scanning is suited for security audits or troubleshooting specific devices (e.g., servers, IoT devices).

2. Pinging (Custom) a Specific IP
    Ping is a foundational network utility to test connectivity and latency. This menu offers advanced customization for tailored diagnostics.
    - How It Works:
        The tool uses ICMP (Internet Control Message Protocol) to send echo requests to a target IP. Customizations include adjusting packet size, timeout durations, and flood pinging.
        Flood Ping: Sends a high volume of packets in quick succession to test network resilience or simulate Denial-of-Service (DoS) conditions (use with extreme caution).
    - When to Use:
        Basic ping to verify if a host is online.
        Custom packet sizes to diagnose MTU (Maximum Transmission Unit) issues.
        Flood ping for stress-testing networks (ethical and controlled environments only).

3. TraceRouting
    TraceRoute maps the path packets take to reach a target IP, showing each hop (router/gateway) along the way
    - How It Works:
        Uses a combination of ICMP, UDP, or TCP packets with incrementally increasing TTL (Time-to-Live) values to identify each hop.
    - When to Use:
        Diagnose network latency issues.
        Identify misconfigured routers or network bottlenecks.

4. Advance Scan
    A suite of professional-grade scanning techniques powered by Nmap for in-depth network analysis.
    - How It Works:
        Nmap Integration: Executes advanced scans such as SYN (stealth), UDP, OS detection, and version scanning. These methods go beyond basic port checks to gather detailed intelligence about target systems.
    - When to Use:
        SYN Scan: For stealthy port scanning without completing full TCP handshakes.
        UDP Scan: To identify open UDP ports (commonly used by DNS, DHCP, and VoIP services).
        OS Detection: To fingerprint the operating system of a remote device.
        Aggressive Scan: Combines multiple techniques for a holistic view of the target (slower but thorough).

Additional Commands
    H (Help): Displays this documentation.
    X (Exit): Safely terminates the program.

Important Notes
    - Ensure Ethical Use:
        Always obtain explicit permission before scanning networks or devices you do not own. Unauthorized scanning may violate local laws.
        Flood ping and DoS-related features should only be used in controlled environments (e.g., penetration testing labs).
    - Performance Tips:
        ARP scans are fastest for local network discovery.
        Nmap scans can be resource-intensive; adjust thread counts and timeouts for large networks.
    - Dependencies:
        Requires root/sudo privileges for ARP, SYN, and flood ping operations.
        Ensure Nmap and Python dependencies are installed (see requirements.txt).

© Kartik | Licensed for Ethical Use Only
"""

help1 = r"""
Selected Option 1: Scanning Full Network, Finding Specific Target
This menu provides two methods to identify and analyze devices on your network.

1. Scan All IPs (High Speed, Less Detailed)
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
    Limitations:
        - No port or service details.
        - Limited to the local subnet.

2. Scan Specific IPs (Slow Speed, More Detailed)
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
Feature	      | Scan All IPs (ARP)  | Scan Specific IPs (Nmap)
--------------|---------------------|--------------------------------
Speed	      | Instant	            | Slow to Moderate
Detail Level  | Basic (IP + MAC)    | Advanced (Ports, Services, OS)
Network Scope | Local Subnet Only   | Any Reachable IP/Subnet
Privileges	  | Requires sudo       | Optional (depends on scan type)

Important Notes
    Ethical Use:
        - Always obtain explicit permission before scanning. Unauthorized scanning may violate privacy laws.
        - ARP scans are passive and less intrusive. Nmap scans may trigger security alerts.
    
    Performance Tips:
        - For ARP scans, avoid overlapping with other network-heavy tasks.
        - For Nmap, narrow IP ranges to reduce scan time (e.g., 192.168.1.1-20).
    
    Dependencies:
        - ARP Scan: Requires scapy Python library.
        - Nmap Scan: Requires nmap installed on the system.

To Return to the Main Menu, press 0.
For Sub-Option Help, type H within any feature.

© Kartik | Licensed for Ethical Use Only
"""

help2 = r"""
Selected Option 2: Pinging (Custom) a Specific IP
This menu allows advanced customization of ICMP (Internet Control Message Protocol) ping requests to diagnose connectivity, test network performance, or simulate stress conditions.

1. Simple Finite Ping
    Purpose: Basic connectivity check to verify if a target IP is reachable.
    Technical Details:
        Method: Standard ICMP echo request/reply.
        Default Settings:
            - Packet Size: 56 bytes (64 bytes with headers).
            - Timeout: 2 seconds per reply.
            - Number of Request: 7 only, for stopping condition
    When to Use:
        - Confirm if a device is online (e.g., router, server).
        - Measure average latency (round-trip time).

2. Large Ping
    Purpose: Test network performance with oversized packets.
    Technical Details:
    Method: Sends ICMP packets with user-defined sizes.
    Customization: 
        - Packet size: Packet sizes will be size of 65,500 bytes (largest possible).
        - Number of Request: Infinite
    Use Case:
        - Diagnose packet fragmentation issues.
        - Test maximum transmission unit (MTU) compatibility.
    Note: Extremely large packets may be dropped by routers or firewalls.

3. Ping for Slow Network
    Purpose: Adjust timeout for high-latency networks.
    Technical Details:
        Method: Increases the wait time for ICMP replies.
        Customization: Timeout can be set to 1–30 seconds.
    Use Case:
        - Diagnose satellite/WAN links with high latency.
        - Test connectivity over unstable connections (e.g., mobile networks).

4. Flood Ping (Requires Sudo)
    Purpose: Stress-test a target by flooding it with ICMP packets.(Linux/macOS only).
    Technical Details:
    Method: Sends packets as fast as possible (DoS simulation).
    Requirements:
        - sudo/root privileges.
        - Linux/macOS only (not supported on Windows).
    Use Case:
        - Test network/server resilience under heavy load.
        - Ethical Note: Only use on authorized networks!
    Warnings:
        - May degrade network performance or trigger security alerts.
        - Flooding public IPs is illegal without explicit permission.

Key Notes
    Ethical Use:
        - Flood Ping is a high-risk feature. Obtain written consent before use.
        - Avoid targeting critical infrastructure (e.g., hospitals, ISPs).
    Performance Tips:
        - For large pings, start with 1500 bytes to test MTU.
        - Use flood pings sparingly (1-5 seconds max).
    Dependencies:
        - Requires system-level ping utility.
        - Flood Ping requires UNIX-based OS (Linux/macOS).

To Return to the Main Menu, press 0.
For Sub-Option Help, type H within any feature.

© Kartik | Licensed for Ethical Use Only
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
    1. 80/TCP - HTTP (Web traffic)  
    2. 443/TCP - HTTPS (Secure web traffic)  
    3. 22/TCP - SSH (Secure Shell)  
    4. 53/TCP/UDP - DNS (Domain Name System)  
    5. 25/TCP - SMTP (Email delivery)  
    6. 110/TCP - POP3 (Email retrieval)  
    7. 143/TCP - IMAP (Email management)  
    8. 21/TCP - FTP Control (File Transfer Protocol)  
    9. 23/TCP - Telnet (Unencrypted remote access)  
    10. 3389/TCP - RDP (Remote Desktop Protocol)  
    11. 445/TCP - SMB (Windows file/printer sharing)  
    12. 139/TCP - NetBIOS Session Service  
    13. 137/UDP - NetBIOS Name Service  
    14. 138/UDP - NetBIOS Datagram Service  
    15. 3306/TCP - MySQL Database  
    16. 5432/TCP - PostgreSQL Database  
    17. 587/TCP - SMTP Submission (Secure email sending)  
    18. 993/TCP - IMAPS (IMAP over SSL)  
    19. 995/TCP - POP3S (POP3 over SSL)  
    20. 161/UDP - SNMP (Network monitoring)  
    21. 162/UDP - SNMP Trap (SNMP alerts)  
    22. 123/UDP - NTP (Network Time Protocol)  
    23. 514/UDP - Syslog (Logging service)  
    24. 67/UDP - DHCP Server (IP assignment)  
    25. 68/UDP - DHCP Client  
    26. 389/TCP/UDP - LDAP (Directory services)  
    27. 636/TCP - LDAPS (LDAP over SSL)  
    28. 8443/TCP - HTTPS Alternate (Common for web apps)  
    29. 8080/TCP - HTTP Alternate (Proxy/web caching)  
    30. 27017/TCP - MongoDB Database  
    31. 6379/TCP - Redis (In-memory database)  
    32. 11211/TCP/UDP - Memcached (Caching system)  
    33. 1194/UDP - OpenVPN  
    34. 500/UDP - IKE (IPsec key exchange)  
    35. 4500/UDP - IPsec NAT-Traversal  
    36. 1433/TCP - Microsoft SQL Server  
    37. 1521/TCP - Oracle Database  
    38. 2049/TCP/UDP - NFS (Network File System)  
    39. 873/TCP - Rsync (File synchronization)  
    40. 5060/TCP/UDP - SIP (VoIP signaling)  
    41. 5061/TCP - SIP-TLS (Secure SIP)  
    42. 5900/TCP - VNC (Remote desktop)  
    43. 25565/TCP - Minecraft Server  
    44. 3128/TCP - Squid Proxy  
    45. 69/UDP - TFTP (Trivial File Transfer Protocol)  
    46. 2222/TCP - SSH Alternate (Custom deployments)  
    47. 9200/TCP - Elasticsearch (Search engine)  
    48. 9300/TCP - Elasticsearch Cluster Communication  
    49. 5601/TCP - Kibana (Data visualization for Elasticsearch)  
    50. 2483/TCP - Oracle Database SSL 

Key Notes
    - TCP vs. UDP: Some services use both (e.g., DNS, LDAP), while others are UDP-only (e.g., DHCP, SNMP, NTP).  
    - Legacy Protocols: Ports like Telnet (23) and FTP (21) are insecure and often replaced by SSH (22) and SFTP/SCP.  
    - Security: Ports like 443 (HTTPS), 993 (IMAPS), and 995 (POP3S) encrypt traffic by default.  
    - Dynamic/Ephemeral Ports: Client-side ports (e.g., 49152–65535) are temporary and not listed here.  
"""
