import os
import sys
import subprocess
import importlib.util
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIREMENTS_PATH = os.path.join(BASE_DIR, "requirements.txt")
MARKER_PATH = os.path.join(BASE_DIR, ".modules_installed_marker")

def is_module_installed(module_name):
    return importlib.util.find_spec(module_name) is not None

def install_module(module_name):
    subprocess.run([sys.executable, "-m", "pip", "install", module_name], check=True)

def extract_module_name(module_line):
    return re.split(r'[<>=~!]+', module_line)[0].strip()

def install_requirements_once():
    if os.path.exists(MARKER_PATH):
        print("[✓] Modules already installed. Skipping installation.")
        return

    if not os.path.exists(REQUIREMENTS_PATH):
        print("[✗] requirements.txt not found!")
        return

    with open(REQUIREMENTS_PATH, "r") as req_file:
        modules = [line.strip() for line in req_file if line.strip() and not line.startswith("#")]

    for module in modules:
        mod_name = extract_module_name(module)
        if not is_module_installed(mod_name):
            print(f"[+] Installing {module}...")
            install_module(module)
        else:
            print(f"[✓] {mod_name} is already installed.")

    with open(MARKER_PATH, "w") as f:
        f.write("installed")

    print("[✓] All required modules are now installed.")


if __name__ == "__main__":
    # This file is not meant to be run directly
    # It should be imported and used in main.py
    # If this file is run directly, it will print an error message
    print("Wrong file selected for running\nPlease run 'main.py' file by using 'python main.py' command")
