import os
import platform
import utils.documentation_utils as doc_utils

Oper_system = platform.system()
oper_system = Oper_system.lower()

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
''')
    print(f"## Welcome to Kartik's OmniScanner ({Oper_system} Version)")


def clear_screen():
    """Clearing the screen before running"""
    os.system('cls' if os.name == 'nt' else 'clear')


def documentation(i):
    """To print documentation from documentation_utils.
    :param : 0 for main menu, 1 for level 1, 2 for level 2, 4 for level 4, p for ports
    :return : Documentation as string"""

    if i == 0:
        return doc_utils.help0
    elif i == 1:
        return doc_utils.help1
    elif i == 2:
        return doc_utils.help2
    elif i == 4:
        return doc_utils.help4
    elif i == 'p':
        return doc_utils.ports
    else:
        return "Documentation not available"
