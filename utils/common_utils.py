import os
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
