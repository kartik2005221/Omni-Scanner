"""
Unified menu engine to eliminate duplication between Linux and Windows scripts.
Provides a generic, configurable menu system that can be used across platforms.
"""
import time
from typing import Dict, List, Callable, Optional, Any
from utils.common_utils import shell, documentation, clear_screen
from utils.logging_utils import get_default_logger


class MenuOption:
    """Represents a single menu option."""
    
    def __init__(self, key: str, description: str, handler: Callable, enabled: bool = True):
        self.key = key.lower()
        self.description = description
        self.handler = handler
        self.enabled = enabled


class MenuEngine:
    """Generic menu engine for consistent menu handling across platforms."""
    
    def __init__(self, title: str = "", delay: float = 0.3):
        self.title = title
        self.delay = delay
        self.options: Dict[str, MenuOption] = {}
        self.logger = get_default_logger()
        
        # Add standard options
        self.add_option("h", "Help", self._show_help)
        self.add_option("0", "Back", self._go_back)
    
    def add_option(self, key: str, description: str, handler: Callable, enabled: bool = True):
        """Add a menu option."""
        self.options[key.lower()] = MenuOption(key, description, handler, enabled)
    
    def remove_option(self, key: str):
        """Remove a menu option."""
        if key.lower() in self.options:
            del self.options[key.lower()]
    
    def enable_option(self, key: str, enabled: bool = True):
        """Enable or disable a menu option."""
        if key.lower() in self.options:
            self.options[key.lower()].enabled = enabled
    
    def display_menu(self):
        """Display the menu options."""
        if self.title:
            print(f"\n{self.title}")
        
        print("\nSelect an Option:")
        
        # Sort options by key, but keep help and back at the end
        sorted_options = []
        regular_options = []
        special_options = []
        
        for option in self.options.values():
            if option.enabled:
                if option.key in ['h', '0']:
                    special_options.append(option)
                else:
                    regular_options.append(option)
        
        # Sort regular options by key
        regular_options.sort(key=lambda x: x.key)
        
        # Display regular options
        for option in regular_options:
            print(f"    [{option.key.upper()}] {option.description}")
        
        # Display special options (Help, Back)
        if special_options:
            help_options = [opt for opt in special_options if opt.key == 'h']
            back_options = [opt for opt in special_options if opt.key == '0']
            
            help_back_line = "    "
            if help_options:
                help_back_line += f"[H] {help_options[0].description}"
            if back_options:
                if help_options:
                    help_back_line += "        "
                help_back_line += f"[0] {back_options[0].description}"
            
            print(help_back_line)
        
        print()
    
    def get_user_input(self, prompt: str = None) -> str:
        """Get user input with optional custom prompt."""
        if prompt is None:
            prompt = shell
        return input(prompt).lower().strip() or '0'
    
    def handle_selection(self, selection: str) -> bool:
        """
        Handle user selection.
        
        Returns:
            bool: True to continue the menu loop, False to exit
        """
        if selection in self.options:
            option = self.options[selection]
            if option.enabled:
                try:
                    result = option.handler()
                    # If handler returns False, exit the menu
                    if result is False:
                        return False
                except Exception as e:
                    self.logger.error(f"Error executing menu option {selection}: {e}")
                    print(f"\nError: {e}")
            else:
                print(f"\nOption '{selection.upper()}' is currently disabled")
        else:
            print(f"\nUnsupported option '{selection.upper()}', please try again")
        
        return True
    
    def run(self) -> int:
        """
        Run the menu loop.
        
        Returns:
            int: Exit code (0 for normal exit, 1 for error)
        """
        try:
            while True:
                self.display_menu()
                selection = self.get_user_input()
                
                if not self.handle_selection(selection):
                    break
                
                time.sleep(self.delay)
            
            return 0
        
        except KeyboardInterrupt:
            print("\n\nExiting...")
            return 0
        except Exception as e:
            self.logger.error(f"Menu error: {e}")
            print(f"\nUnexpected error: {e}")
            return 1
    
    def _show_help(self):
        """Default help handler."""
        print(documentation(1))
        input("Press Enter to continue...")
    
    def _go_back(self):
        """Default back handler."""
        return False  # Signal to exit the menu


class ScanMenuBuilder:
    """Helper class to build scan-specific menus."""
    
    @staticmethod
    def create_arp_menu(platform: str = "linux") -> MenuEngine:
        """Create ARP scan menu."""
        menu = MenuEngine("ARP Scanner")
        
        from utils.scan_builders import build_arp_scan_cmd, build_nmap_arp_scan_cmd
        from utils.common_utils import run_command_save
        from utils.administrative_utils import is_sudo_linux
        from utils.menu_utils import validate_ip
        
        def local_arp_scan():
            if platform == "linux" and not is_sudo_linux():
                print("\nSudo not detected, \nTry another option or Switch to SUDO")
                return
            
            cmd = build_arp_scan_cmd(sudo_required=True)
            run_command_save(cmd, "arp-scan")
        
        def target_arp_scan():
            ip_addr = input(f"\nEnter range of IPs\n{shell}") or "127.0.0.1"
            if validate_ip(ip_addr):
                cmd = build_nmap_arp_scan_cmd(ip_addr)
                run_command_save(cmd, "arp-scan")
            else:
                print("\nInvalid IP Address, please try again")
        
        menu.add_option("1", "Arp scan: All IPs on network (requires sudo)", local_arp_scan)
        menu.add_option("2", "Nmap-Arp scan: Specific IP(s)", target_arp_scan)
        
        return menu
    
    @staticmethod
    def create_ping_menu(platform: str = "linux") -> MenuEngine:
        """Create ping menu."""
        menu = MenuEngine("Ping Scanner")
        
        from utils.scan_builders import build_ping_cmd
        from utils.common_utils import run_command_save
        from utils.administrative_utils import is_sudo_linux
        from utils.menu_utils import validate_ip, parse_scan_options
        
        def handle_ping_options():
            """Handle ping with various options."""
            print("""
Select required options (separate by space):
    [1] Simple ping — use alone, not with other options
    [2] Bigger packet size of ping
    [3] Slow-network ping
    [4] Flood ping (sudo required)""")
            
            options_input = input(f"\n{shell}") or "1"
            options = parse_scan_options(options_input)
            
            target = input(f"\nEnter target IP\n{shell}") or "127.0.0.1"
            if not validate_ip(target):
                print("\nInvalid IP Address, please try again")
                return
            
            # Parse options
            packet_size = None
            timeout = None
            flood = False
            count = 5
            
            if "2" in options:
                size_input = input(f"\nEnter size of packet to send (0-65500)\n{shell}") or "56"
                packet_size = int(size_input) if size_input.isdigit() else 56
            
            if "3" in options:
                timeout_input = input(f"\nHow much time(sec.) to wait?\n{shell}") or "1"
                timeout = float(timeout_input) if timeout_input.replace('.', '').isdigit() else 1.0
            
            if "4" in options:
                flood = True
                if platform == "linux" and not is_sudo_linux():
                    print("\nSudo not detected, Try another option or Switch to SUDO")
                    return
            
            # Ask for finite or infinite ping
            ping_type = input(f"\nPing finitely or infinitely? (1/2)\n{shell}") or "1"
            infinite = ping_type == "2"
            
            if not infinite:
                count_input = input(f"\nEnter number of packets to send\n{shell}") or "5"
                count = int(count_input) if count_input.isdigit() else 5
            
            # Build and execute command
            cmd = build_ping_cmd(
                target=target,
                count=count if not infinite else None,
                packet_size=packet_size,
                timeout=timeout,
                flood=flood,
                infinite=infinite,
                sudo_required=is_sudo_linux() if platform == "linux" else False
            )
            
            run_command_save(cmd, "ping-scan")
        
        menu.add_option("1", "Ping with options", handle_ping_options)
        
        return menu
    
    @staticmethod
    def create_traceroute_menu(platform: str = "linux") -> MenuEngine:
        """Create traceroute menu."""
        menu = MenuEngine("Traceroute Scanner")
        
        from utils.scan_builders import build_traceroute_cmd
        from utils.common_utils import run_command_save
        from utils.menu_utils import validate_ip
        
        def simple_traceroute():
            target = input(f"\nEnter target IP/hostname\n{shell}") or "8.8.8.8"
            if validate_ip(target.split('/')[0]):  # Handle potential CIDR
                cmd = build_traceroute_cmd(target)
                run_command_save(cmd, "traceroute-scan")
            else:
                print("\nInvalid target, please try again")
        
        def advanced_traceroute():
            target = input(f"\nEnter target IP/hostname\n{shell}") or "8.8.8.8"
            if not validate_ip(target.split('/')[0]):
                print("\nInvalid target, please try again")
                return
            
            max_hops_input = input(f"\nMax hops (default 30)\n{shell}") or "30"
            max_hops = int(max_hops_input) if max_hops_input.isdigit() else 30
            
            timeout_input = input(f"\nTimeout per hop in seconds (default 5)\n{shell}") or "5"
            timeout = float(timeout_input) if timeout_input.replace('.', '').isdigit() else 5.0
            
            cmd = build_traceroute_cmd(target, max_hops=max_hops, timeout=timeout)
            run_command_save(cmd, "traceroute-scan")
        
        menu.add_option("1", "Simple traceroute", simple_traceroute)
        menu.add_option("2", "Advanced traceroute with options", advanced_traceroute)
        
        return menu
    
    @staticmethod
    def create_nmap_menu(platform: str = "linux") -> MenuEngine:
        """Create Nmap menu."""
        menu = MenuEngine("Nmap Scanner")
        
        from utils.scan_builders import build_nmap_scan_cmd, build_nmap_firewall_scan_cmd
        from utils.common_utils import run_command_save
        from utils.menu_utils import validate_ip, validate_port_range
        
        def basic_nmap_scan():
            target = input(f"\nEnter target IP/network\n{shell}") or "127.0.0.1"
            if validate_ip(target):
                cmd = build_nmap_scan_cmd(target, scan_type="syn", timing="T4")
                run_command_save(cmd, "nmap-scan")
            else:
                print("\nInvalid target, please try again")
        
        def port_scan():
            target = input(f"\nEnter target IP/network\n{shell}") or "127.0.0.1"
            if not validate_ip(target):
                print("\nInvalid target, please try again")
                return
            
            ports = input(f"\nEnter ports (e.g., 80,443 or 1-1000)\n{shell}") or "1-1000"
            if not validate_port_range(ports):
                print("\nInvalid port specification, please try again")
                return
            
            cmd = build_nmap_scan_cmd(target, ports=ports, timing="T4")
            run_command_save(cmd, "nmap-scan")
        
        def service_detection_scan():
            target = input(f"\nEnter target IP/network\n{shell}") or "127.0.0.1"
            if validate_ip(target):
                cmd = build_nmap_scan_cmd(
                    target, 
                    service_detection=True, 
                    os_detection=True, 
                    timing="T4"
                )
                run_command_save(cmd, "nmap-scan")
            else:
                print("\nInvalid target, please try again")
        
        def firewall_evasion_scan():
            target = input(f"\nEnter target IP\n{shell}") or "127.0.0.1"
            if validate_ip(target):
                cmd = build_nmap_firewall_scan_cmd(target)
                run_command_save(cmd, "nmap-scan")
            else:
                print("\nInvalid target, please try again")
        
        menu.add_option("1", "Basic SYN scan", basic_nmap_scan)
        menu.add_option("2", "Port range scan", port_scan)
        menu.add_option("3", "Service/OS detection scan", service_detection_scan)
        menu.add_option("4", "Firewall evasion scan", firewall_evasion_scan)
        
        return menu