import os
import sys


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def change_title(title):
    sys.stdout.write(f'\33]0;{title}\a')
    sys.stdout.flush()
