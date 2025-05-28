import os
import shutil
import sys


def is_termux():
    """
    Check if the script is running in Termux environment.
    :return: True if running in Termux, False otherwise.
    """
    return 'com.termux' in os.environ.get('PREFIX', '')


def get_platform():
    """Determine the current platform.
    :return: A string representing the platform ('termux', 'linux', 'windows').
    """
    if is_termux():
        return 'termux'
    elif sys.platform.startswith('linux'):
        return 'linux'
    elif sys.platform.startswith('win32'):
        return 'windows'
    else:
        print('Unsupported platform')
        sys.exit(1)


def get_install_paths(current_platform2):
    """Get installation paths based on the current platform.
    :param current_platform2: The platform string ('termux', 'linux', 'windows').
    :return: A dictionary containing installation paths.
    """
    paths = {}
    if current_platform2 == 'termux':
        prefix = os.environ.get('PREFIX')
        paths['install_dir'] = os.path.join(prefix, 'share', 'omni-scanner')
        paths['bin_dir'] = os.path.join(prefix, 'bin')
    elif current_platform2 == 'linux':
        if os.geteuid() == 0:  # Root install
            paths['install_dir'] = '/usr/share/omni-scanner'
            paths['bin_dir'] = '/usr/bin'
        else:  # User install
            home = os.path.expanduser('~')
            paths['install_dir'] = os.path.join(home, '.local', 'share', 'omni-scanner')
            paths['bin_dir'] = os.path.join(home, '.local', 'bin')
    elif current_platform2 == 'windows':
        appdata = os.environ.get('APPDATA')
        paths['install_dir'] = os.path.join(appdata, 'omni-scanner')
        paths['bin_dir'] = os.path.join(os.environ['LOCALAPPDATA'], 'Programs', 'Python', 'Scripts')

    paths['launcher_path'] = os.path.join(paths['bin_dir'],
                                          'omni-scanner.bat' if current_platform2 == 'windows' else 'omni-scanner')
    return paths


# def install_dependencies():
#     """Install required Python packages from requirements.txt."""
#     req_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
#     if os.path.exists(req_file):
#         os.system(f'"{sys.executable}" -m pip install -r "{req_file}"')


def create_launcher(current_platform3, paths):
    """Create a launcher script for the Omni-Scanner application.
    :param current_platform3: The platform string ('termux', 'linux', 'windows').
    :param paths: A dictionary containing installation paths.
    """
    main_script = os.path.join(paths['install_dir'], 'main.py')

    if current_platform3 in ['termux', 'linux']:
        launcher_content = f'''#!/bin/sh
exec "{sys.executable}" "{main_script}" "$@"
'''
    else:  # Windows
        launcher_content = f'''@echo off
"{sys.executable}" "{main_script}" %*
'''

    os.makedirs(paths['bin_dir'], exist_ok=True)
    with open(paths['launcher_path'], 'w') as f:
        f.write(launcher_content)

    if current_platform3 != 'windows':
        os.chmod(paths['launcher_path'], 0o755)


def install(current_platform4):
    """Install the Omni-Scanner application.
    :param current_platform4: The platform string ('termux', 'linux', 'windows').
    """
    paths = get_install_paths(current_platform4)
    source_dir = os.path.dirname(os.path.abspath(__file__))

    # Copy project files
    if os.path.exists(paths['install_dir']):
        shutil.rmtree(paths['install_dir'])
    shutil.copytree(source_dir, paths['install_dir'])

    # Create launcher
    create_launcher(current_platform4, paths)

    # Install requirements
    # install_dependencies()

    print(f'''\n[+] Omni-Scanner installed successfully!
[+] You can now run it using the 'omni-scanner' command{' (you may need to restart your terminal)' if current_platform4 == 'windows' else ''}''')


def uninstall(current_platform5):
    """Uninstall the Omni-Scanner application.
    :param current_platform5: The platform string ('termux', 'linux', 'windows').
    """
    paths = get_install_paths(current_platform5)

    if os.path.exists(paths['install_dir']):
        shutil.rmtree(paths['install_dir'])
    if os.path.exists(paths['launcher_path']):
        os.remove(paths['launcher_path'])

    print('[!] Omni-Scanner has been removed successfully')


if __name__ == '__main__':
    current_platform = get_platform()

    if current_platform == 'linux' and os.geteuid() != 0:
        print('For system-wide installation, run with sudo. For user installation, continue.')

    choice = input('[+] To install press (Y) to uninstall press (N) >> ').lower()

    if choice == 'y':
        install(current_platform)
    elif choice == 'n':
        uninstall(current_platform)
    else:
        print('Invalid choice')
        sys.exit(1)
