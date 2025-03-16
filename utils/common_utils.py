import os
import subprocess
import platform
oper_system = platform.system()

def splash_screen():
    """To print splash screen"""
    print(r'''
kkkkkkkk                                                          tttt            iiii  kkkkkkkk
k::::::k                                                       ttt:::t           i::::i k::::::k
k::::::k                                                       t:::::t            iiii  k::::::k
k::::::k                                                       t:::::t                  k::::::k
 k:::::k    kkkkkkk  aaaaaaaaaaaaa   rrrrr   rrrrrrrrr   ttttttt:::::ttttttt    iiiiiii  k:::::k    kkkkkkk
 k:::::k   k:::::k   a::::::::::::a  r::::rrr:::::::::r  t:::::::::::::::::t    i:::::i  k:::::k   k:::::k
 k:::::k  k:::::k    aaaaaaaaa:::::a r:::::::::::::::::r t:::::::::::::::::t     i::::i  k:::::k  k:::::k
 k:::::k k:::::k              a::::a rr::::::rrrrr::::::rtttttt:::::::tttttt     i::::i  k:::::k k:::::k
 k::::::k:::::k        aaaaaaa:::::a  r:::::r     r:::::r      t:::::t           i::::i  k::::::k:::::k
 k:::::::::::k       aa::::::::::::a  r:::::r     rrrrrrr      t:::::t           i::::i  k:::::::::::k
 k:::::::::::k      a::::aaaa::::::a  r:::::r                  t:::::t           i::::i  k:::::::::::k
 k::::::k:::::k    a::::a    a:::::a  r:::::r                  t:::::t    tttttt i::::i  k::::::k:::::k
k::::::k k:::::k   a::::a    a:::::a  r:::::r                  t::::::tttt:::::ti::::::ik::::::k k:::::k
k::::::k  k:::::k  a:::::aaaa::::::a  r:::::r                  tt::::::::::::::ti::::::ik::::::k  k:::::k
k::::::k   k:::::k  a::::::::::aa:::a r:::::r                    tt:::::::::::tti::::::ik::::::k   k:::::k
kkkkkkkk    kkkkkkk  aaaaaaaaaa  aaaa rrrrrrr                      ttttttttttt  iiiiiiiikkkkkkkk    kkkkkkk


***********************************************************************
***********************************************************************
****                                                               ****
****                © Copyright of Kartik - 2025                   ****
****                                                               ****
***********************************************************************
*****************************************************[Ethical Use Only]

## Welcome to Kartik's OmniScanner''')


def clear_screen():
    """Clearing the screen before running"""
    os.system('cls' if os.name == 'nt' else 'clear')


def check_sudo():
    """To check for current program is running with sudo or not,
    0 -> no sudo,
    1 -> sudo"""
    if not 'SUDO_UID' in os.environ.keys():
        return 0
    else:
        return 1


def run_with_sudo():
    """To Run again program with sudo.
    first take input from user, if he wants to run again with sudo or not"""
    if input("Press 0 if you want to exit and run again with sudo\nElse, Press any key...\n: ") == '0':
        if oper_system.lower() == 'linux':
            subprocess.run(["sudo", "-S", "python", os.path.basename(__file__)])
        elif oper_system.lower() == 'windows':
            subprocess.run(["sudo", "python", os.path.basename(__file__)])
        exit()
