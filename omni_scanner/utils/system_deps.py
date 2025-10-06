"""
System Dependencies Installer - Checks and installs required system tools.
"""
import subprocess
import shutil
import sys
import os
from typing import List, Dict, Tuple
from .logging import get_logger

logger = get_logger(__name__)


class SystemDependencyInstaller:
    """System dependency installer for various Linux distributions."""
    
    def __init__(self):
        self.platform = self._detect_platform()
        self.package_manager = self._detect_package_manager()
        
        # Required system dependencies
        self.dependencies = {
            'nmap': {
                'check_cmd': ['nmap', '--version'],
                'packages': {
                    'apt': 'nmap',
                    'dnf': 'nmap',
                    'pacman': 'nmap',
                    'brew': 'nmap',
                    'pkg': 'nmap'  # Termux
                },
                'description': 'Network exploration tool and security scanner'
            },
            'arp-scan': {
                'check_cmd': ['arp-scan', '--version'],
                'packages': {
                    'apt': 'arp-scan',
                    'dnf': 'arp-scan',
                    'pacman': 'arp-scan',
                    'brew': 'arp-scan',
                    'pkg': 'arp-scan'  # Termux
                },
                'description': 'ARP scanning and fingerprinting tool'
            },
            'traceroute': {
                'check_cmd': ['traceroute', '--version'],
                'packages': {
                    'apt': 'traceroute',
                    'dnf': 'traceroute',
                    'pacman': 'traceroute',
                    'brew': 'traceroute',
                    'pkg': 'traceroute'  # Termux
                },
                'description': 'Network diagnostic tool for tracing packets'
            },
            'ping': {
                'check_cmd': ['ping', '-V'],
                'packages': {
                    'apt': 'iputils-ping',
                    'dnf': 'iputils',
                    'pacman': 'iputils',
                    'brew': None,  # Built-in on macOS
                    'pkg': 'iputils'  # Termux
                },
                'description': 'Network connectivity testing tool'
            }
        }
    
    def _detect_platform(self) -> str:
        """Detect the current platform."""
        if 'com.termux' in os.environ.get('PREFIX', ''):
            return 'termux'
        elif sys.platform.startswith('linux'):
            return 'linux'
        elif sys.platform.startswith('darwin'):
            return 'macos'
        elif sys.platform.startswith('win'):
            return 'windows'
        else:
            return 'unknown'
    
    def _detect_package_manager(self) -> str:
        """Detect the available package manager."""
        package_managers = {
            'apt': ['apt', 'apt-get'],
            'dnf': ['dnf'],
            'pacman': ['pacman'],
            'brew': ['brew'],
            'pkg': ['pkg']  # Termux
        }
        
        for pm, commands in package_managers.items():
            for cmd in commands:
                if shutil.which(cmd):
                    return pm
        
        return 'unknown'
    
    def check_dependency(self, tool: str) -> bool:
        """
        Check if a dependency is installed.
        
        Args:
            tool: Tool name to check
            
        Returns:
            bool: True if tool is installed and working
        """
        if tool not in self.dependencies:
            logger.warning(f"Unknown dependency: {tool}")
            return False
        
        check_cmd = self.dependencies[tool]['check_cmd']
        
        try:
            # First check if command exists
            if not shutil.which(check_cmd[0]):
                return False
            
            # Then check if it works
            result = subprocess.run(
                check_cmd, 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def check_all_dependencies(self) -> Dict[str, bool]:
        """
        Check all required dependencies.
        
        Returns:
            Dict[str, bool]: Mapping of tool names to their availability
        """
        results = {}
        for tool in self.dependencies:
            results[tool] = self.check_dependency(tool)
            status = "✅ Available" if results[tool] else "❌ Missing"
            logger.info(f"{tool}: {status}")
        
        return results
    
    def install_dependency(self, tool: str, sudo: bool = True) -> Tuple[bool, str]:
        """
        Install a single dependency.
        
        Args:
            tool: Tool name to install
            sudo: Use sudo for installation
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        if tool not in self.dependencies:
            return False, f"Unknown dependency: {tool}"
        
        if self.package_manager == 'unknown':
            return False, "No supported package manager found"
        
        package_name = self.dependencies[tool]['packages'].get(self.package_manager)
        
        if not package_name:
            return False, f"{tool} not available for {self.package_manager}"
        
        # Build install command
        if self.package_manager == 'apt':
            cmd = ['apt', 'update', '&&', 'apt', 'install', '-y', package_name]
            if sudo and os.geteuid() != 0:
                cmd = ['sudo'] + cmd
        elif self.package_manager == 'dnf':
            cmd = ['dnf', 'install', '-y', package_name]
            if sudo and os.geteuid() != 0:
                cmd = ['sudo'] + cmd
        elif self.package_manager == 'pacman':
            cmd = ['pacman', '-S', '--noconfirm', package_name]
            if sudo and os.geteuid() != 0:
                cmd = ['sudo'] + cmd
        elif self.package_manager == 'brew':
            cmd = ['brew', 'install', package_name]
        elif self.package_manager == 'pkg':  # Termux
            cmd = ['pkg', 'install', '-y', package_name]
        else:
            return False, f"Installation not implemented for {self.package_manager}"
        
        try:
            logger.info(f"Installing {tool} using {self.package_manager}...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                logger.info(f"Successfully installed {tool}")
                return True, f"Successfully installed {tool}"
            else:
                error_msg = result.stderr or result.stdout
                logger.error(f"Failed to install {tool}: {error_msg}")
                return False, f"Failed to install {tool}: {error_msg}"
                
        except subprocess.TimeoutExpired:
            return False, f"Installation of {tool} timed out"
        except Exception as e:
            return False, f"Installation error: {str(e)}"
    
    def install_missing_dependencies(self, missing_tools: List[str] = None, 
                                   auto_install: bool = False) -> Dict[str, Tuple[bool, str]]:
        """
        Install missing dependencies.
        
        Args:
            missing_tools: List of tools to install, or None for all missing
            auto_install: Install without user confirmation
            
        Returns:
            Dict[str, Tuple[bool, str]]: Installation results
        """
        if missing_tools is None:
            # Check all dependencies and find missing ones
            status = self.check_all_dependencies()
            missing_tools = [tool for tool, available in status.items() if not available]
        
        if not missing_tools:
            logger.info("All dependencies are already installed!")
            return {}
        
        results = {}
        
        print(f"\n🔧 Missing system dependencies detected:")
        for tool in missing_tools:
            desc = self.dependencies[tool]['description']
            print(f"  • {tool}: {desc}")
        
        if not auto_install:
            if self.platform == 'windows':
                print("\n📝 Please install the required tools manually:")
                print("  • Nmap: https://nmap.org/download.html")
                print("  • For other tools, consider using WSL or install Windows equivalents")
                return results
            
            response = input(f"\nInstall missing dependencies using {self.package_manager}? [y/N]: ")
            if response.lower() not in ['y', 'yes']:
                print("Skipping dependency installation.")
                return results
        
        print(f"\n🚀 Installing dependencies using {self.package_manager}...")
        
        for tool in missing_tools:
            success, message = self.install_dependency(tool)
            results[tool] = (success, message)
            
            if success:
                print(f"  ✅ {tool}: {message}")
            else:
                print(f"  ❌ {tool}: {message}")
        
        # Verify installation
        print("\n🔍 Verifying installations...")
        for tool in missing_tools:
            if self.check_dependency(tool):
                print(f"  ✅ {tool}: Working correctly")
            else:
                print(f"  ❌ {tool}: Still not working")
        
        return results
    
    def get_installation_instructions(self) -> str:
        """
        Get installation instructions for the current platform.
        
        Returns:
            str: Installation instructions
        """
        if self.platform == 'windows':
            return """
🪟 Windows Installation Instructions:

1. Install Nmap:
   - Download from: https://nmap.org/download.html
   - Or use Chocolatey: choco install nmap

2. For ARP scanning and traceroute:
   - Consider using Windows Subsystem for Linux (WSL)
   - Or install Windows equivalents

3. Alternative: Use Docker container with pre-installed tools
"""
        
        elif self.package_manager == 'apt':  # Ubuntu/Debian
            return """
🐧 Ubuntu/Debian Installation:

sudo apt update
sudo apt install -y nmap arp-scan traceroute iputils-ping

Or run: python -m omni_scanner.utils.system_deps --install
"""
        
        elif self.package_manager == 'dnf':  # Fedora/RHEL
            return """
🎩 Fedora/RHEL Installation:

sudo dnf install -y nmap arp-scan traceroute iputils

Or run: python -m omni_scanner.utils.system_deps --install
"""
        
        elif self.package_manager == 'pacman':  # Arch Linux
            return """
🏹 Arch Linux Installation:

sudo pacman -S nmap arp-scan traceroute iputils

Or run: python -m omni_scanner.utils.system_deps --install
"""
        
        elif self.package_manager == 'brew':  # macOS
            return """
🍎 macOS Installation:

brew install nmap arp-scan

Or run: python -m omni_scanner.utils.system_deps --install
"""
        
        elif self.package_manager == 'pkg':  # Termux
            return """
📱 Termux Installation:

pkg install -y nmap arp-scan traceroute iputils

Or run: python -m omni_scanner.utils.system_deps --install
"""
        
        else:
            return """
❓ Unknown platform. Please install these tools manually:
- nmap: Network scanner
- arp-scan: ARP scanner  
- traceroute: Network path tracer
- ping: Connectivity tester
"""


def main():
    """Main entry point for dependency installer."""
    import argparse
    
    parser = argparse.ArgumentParser(description="System Dependencies Manager for Omni-Scanner")
    parser.add_argument('--check', action='store_true', help='Check dependency status')
    parser.add_argument('--install', action='store_true', help='Install missing dependencies')
    parser.add_argument('--auto', action='store_true', help='Auto-install without confirmation')
    parser.add_argument('--instructions', action='store_true', help='Show installation instructions')
    
    args = parser.parse_args()
    
    installer = SystemDependencyInstaller()
    
    if args.instructions:
        print(installer.get_installation_instructions())
        return
    
    if args.check or not any([args.install, args.instructions]):
        print("🔍 Checking system dependencies...")
        status = installer.check_all_dependencies()
        
        missing = [tool for tool, available in status.items() if not available]
        if missing:
            print(f"\n❌ Missing dependencies: {', '.join(missing)}")
            print("\nRun with --install to install missing dependencies")
            print("Or use --instructions for manual installation steps")
        else:
            print("\n✅ All dependencies are installed!")
    
    if args.install:
        installer.install_missing_dependencies(auto_install=args.auto)


if __name__ == '__main__':
    main()