#!/usr/bin/env python3
"""
Omni-Scanner Auto Setup Script
==============================

This script automatically:
1. Detects the operating system
2. Creates a virtual environment (.venv)
3. Installs all required dependencies
4. Provides instructions for activation

Supports: Windows, Linux, macOS
"""

import os
import sys
import subprocess
import platform
import venv
from pathlib import Path

class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_colored(message, color=Colors.WHITE):
    """Print colored message to console"""
    try:
        print(f"{color}{message}{Colors.END}")
    except UnicodeEncodeError:
        # Fallback for Windows console encoding issues
        print(message.encode('ascii', 'replace').decode('ascii'))

def print_header():
    """Print script header"""
    print_colored("=" * 60, Colors.CYAN)
    print_colored("🚀 OMNI-SCANNER AUTO SETUP", Colors.BOLD + Colors.CYAN)
    print_colored("=" * 60, Colors.CYAN)
    print()

def detect_os():
    """Detect the operating system"""
    # Check for Termux first (Android terminal emulator)
    if 'com.termux' in os.environ.get('PREFIX', ''):
        print_colored("🤖 Detected: Termux (Android)", Colors.BLUE)
        return "termux"
    
    system = platform.system().lower()
    print_colored(f"🔍 Detected OS: {platform.system()} {platform.release()}", Colors.BLUE)
    
    if system == "windows":
        return "windows"
    elif system in ["linux", "darwin"]:
        return "unix"
    else:
        print_colored(f"⚠️  Unknown OS: {system}. Treating as Unix-like.", Colors.YELLOW)
        return "unix"

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print_colored(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}", Colors.BLUE)
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_colored("❌ Error: Python 3.8+ is required!", Colors.RED)
        print_colored("Please upgrade Python and try again.", Colors.RED)
        return False
    
    print_colored("✅ Python version is compatible", Colors.GREEN)
    return True

def create_virtual_environment():
    """Create virtual environment"""
    venv_path = Path(".venv")
    
    if venv_path.exists():
        print_colored("📁 Virtual environment already exists", Colors.YELLOW)
        response = input("Do you want to recreate it? (y/N): ").lower().strip()
        if response in ['y', 'yes']:
            print_colored("🗑️  Removing existing virtual environment...", Colors.YELLOW)
            import shutil
            shutil.rmtree(venv_path)
        else:
            print_colored("✅ Using existing virtual environment", Colors.GREEN)
            return True
    
    print_colored("🔨 Creating virtual environment...", Colors.CYAN)
    try:
        venv.create(".venv", with_pip=True)
        print_colored("✅ Virtual environment created successfully", Colors.GREEN)
        return True
    except Exception as e:
        print_colored(f"❌ Failed to create virtual environment: {e}", Colors.RED)
        return False

def get_activation_command(os_type):
    """Get the activation command for the virtual environment"""
    if os_type == "windows":
        return ".venv\\Scripts\\activate"
    else:
        return "source .venv/bin/activate"

def get_python_executable(os_type):
    """Get the Python executable path in virtual environment"""
    if os_type == "windows":
        return ".venv\\Scripts\\python.exe"
    else:
        return ".venv/bin/python"

def install_requirements(os_type):
    """Install requirements from requirements.txt"""
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print_colored("❌ requirements.txt not found!", Colors.RED)
        return False
    
    python_exe = get_python_executable(os_type)
    
    print_colored("📦 Installing requirements...", Colors.CYAN)
    try:
        # Upgrade pip first
        print_colored("🔄 Upgrading pip...", Colors.BLUE)
        subprocess.run([python_exe, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # Install requirements
        print_colored("📋 Installing packages from requirements.txt...", Colors.BLUE)
        result = subprocess.run([python_exe, "-m", "pip", "install", "-r", "requirements.txt"], 
                               check=True, capture_output=True, text=True)
        
        print_colored("✅ All requirements installed successfully!", Colors.GREEN)
        return True
        
    except subprocess.CalledProcessError as e:
        print_colored(f"❌ Failed to install requirements: {e}", Colors.RED)
        if e.stdout:
            print_colored(f"STDOUT: {e.stdout}", Colors.YELLOW)
        if e.stderr:
            print_colored(f"STDERR: {e.stderr}", Colors.YELLOW)
        return False

def create_activation_scripts(os_type):
    """Create convenient activation scripts"""
    print_colored("📝 Creating activation scripts...", Colors.CYAN)
    
    if os_type == "windows":
        # Windows batch file
        batch_content = '''@echo off
echo Activating Omni-Scanner virtual environment...
call .venv\\Scripts\\activate.bat
echo.
echo Virtual environment activated!
echo You can now run: python main.py
echo To deactivate, type: deactivate
cmd /k
'''
        with open("activate.bat", "w") as f:
            f.write(batch_content)
        print_colored("Created activate.bat", Colors.GREEN)
        
        # PowerShell script
        ps1_content = '''Write-Host "Activating Omni-Scanner virtual environment..." -ForegroundColor Cyan
.venv\\Scripts\\Activate.ps1
Write-Host ""
Write-Host "Virtual environment activated!" -ForegroundColor Green
Write-Host "You can now run: python main.py" -ForegroundColor Yellow
Write-Host "To deactivate, type: deactivate" -ForegroundColor Blue
'''
        with open("activate.ps1", "w") as f:
            f.write(ps1_content)
        print_colored("Created activate.ps1", Colors.GREEN)
        
    else:
        # Unix shell script
        shell_content = '''#!/bin/bash
echo "Activating Omni-Scanner virtual environment..."
source .venv/bin/activate
echo "Virtual environment activated!"
echo "You can now run: python main.py"
echo "To deactivate, type: deactivate"
exec "$SHELL"
'''
        with open("activate.sh", "w") as f:
            f.write(shell_content)
        
        # Make executable
        os.chmod("activate.sh", 0o755)
        print_colored("Created activate.sh", Colors.GREEN)

def print_success_instructions(os_type):
    """Print final success instructions"""
    print()
    print_colored("SETUP COMPLETED SUCCESSFULLY!", Colors.BOLD + Colors.GREEN)
    print_colored("=" * 60, Colors.GREEN)
    print()
    
    activation_cmd = get_activation_command(os_type)
    
    print_colored("HOW TO USE:", Colors.BOLD + Colors.CYAN)
    print()
    
    if os_type == "windows":
        print_colored("Option 1 - Use activation script:", Colors.YELLOW)
        print_colored("  • Double-click 'activate.bat'", Colors.WHITE)
        print_colored("  • Or run in PowerShell: .\\activate.ps1", Colors.WHITE)
        print()
        print_colored("Option 2 - Manual activation:", Colors.YELLOW)
        print_colored(f"  {activation_cmd}", Colors.WHITE)
        print_colored("  python main.py", Colors.WHITE)
    elif os_type == "termux":
        print_colored("Termux-specific instructions:", Colors.YELLOW)
        print_colored("  ./activate.sh", Colors.WHITE)
        print_colored("  # Or manually:", Colors.WHITE)
        print_colored(f"  {activation_cmd}", Colors.WHITE)
        print_colored("  python main.py", Colors.WHITE)
        print()
        print_colored("📱 Termux Notes:", Colors.CYAN)
        print_colored("  • Install system dependencies: pkg install nmap arp-scan", Colors.WHITE)
        print_colored("  • Some scans may require root (use su or tsu)", Colors.WHITE)
        print_colored("  • Network scanning works on local WiFi networks", Colors.WHITE)
    else:
        print_colored("Option 1 - Use activation script:", Colors.YELLOW)
        print_colored("  ./activate.sh", Colors.WHITE)
        print()
        print_colored("Option 2 - Manual activation:", Colors.YELLOW)
        print_colored(f"  {activation_cmd}", Colors.WHITE)
        print_colored("  python main.py", Colors.WHITE)
    
    print()
    print_colored("TROUBLESHOOTING:", Colors.BOLD + Colors.MAGENTA)
    print_colored("• If you get permission errors, run as administrator/sudo", Colors.WHITE)
    print_colored("• Make sure Python 3.8+ is installed", Colors.WHITE)
    print_colored("• Check that requirements.txt exists", Colors.WHITE)
    print()
    print_colored("Ready to scan networks!", Colors.BOLD + Colors.GREEN)

def check_system_dependencies():
    """Check and warn about missing system dependencies"""
    print_colored("🔍 CHECKING SYSTEM DEPENDENCIES", Colors.BOLD + Colors.YELLOW)
    print_colored("-" * 40, Colors.YELLOW)
    
    try:
        # Import the dependency checker
        sys.path.insert(0, os.path.join(os.getcwd()))
        from omni_scanner.utils.system_deps import SystemDependencyInstaller
        
        installer = SystemDependencyInstaller()
        status = installer.check_all_dependencies()
        
        missing = [tool for tool, available in status.items() if not available]
        
        if missing:
            print_colored(f"⚠️  Missing system tools: {', '.join(missing)}", Colors.YELLOW)
            print_colored("\n📋 To install missing dependencies:", Colors.CYAN)
            
            if installer.platform == 'windows':
                print_colored("   • Install Nmap: https://nmap.org/download.html", Colors.WHITE)
                print_colored("   • For full functionality, consider using WSL", Colors.WHITE)
            else:
                print_colored(f"   • Run: python -m omni_scanner.utils.system_deps --install", Colors.WHITE)
                print_colored(f"   • Or: omni-scanner system-deps --install", Colors.WHITE)
            
            print_colored("\n💡 You can check dependencies anytime with:", Colors.CYAN)
            print_colored("   omni-scanner system-deps --check", Colors.WHITE)
        else:
            print_colored("✅ All system dependencies are available!", Colors.GREEN)
            
    except ImportError as e:
        print_colored("⚠️  Unable to check system dependencies", Colors.YELLOW)
        print_colored("   (This is normal during initial setup)", Colors.WHITE)
    except Exception as e:
        print_colored(f"⚠️  Dependency check failed: {e}", Colors.YELLOW)


def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Detect OS
    os_type = detect_os()
    print()
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    print()
    
    # Install requirements
    if not install_requirements(os_type):
        sys.exit(1)
    print()
    
    # Create activation scripts
    create_activation_scripts(os_type)
    print()
    
    # Check system dependencies
    check_system_dependencies()
    print()
    
    # Print success instructions
    print_success_instructions(os_type)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\n❌ Setup interrupted by user", Colors.RED)
        sys.exit(1)
    except Exception as e:
        print_colored(f"\n\n❌ Unexpected error: {e}", Colors.RED)
        sys.exit(1)