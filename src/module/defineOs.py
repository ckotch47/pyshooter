import subprocess
import sys
import re
from src.module.errorsmsg import *


class check_platform:
    platform = None

    def __init__(self):
        self.defineOs()

    def defineOs(self):
        if sys.platform == 'darwin':
            self.platform = 'darwin'
            return self.platform

        elif sys.platform == 'linux':
            self.platform = 'linux'
            if self.check_gnome_screenhoot():
                return self.platform
            else:
                self.platform = None
                install_gnome_screenshoot()

    @staticmethod
    def check_gnome_screenhoot():
        popen = subprocess.Popen('gnome-screenshot --version', shell=True, stdout=subprocess.PIPE)
        tmp = next(iter(popen.stdout.readline, '')).rstrip().decode('utf-8')  # [gnome]*-[screenshot]* [0-9]*.[0-9]
        if re.match(r'gnome-screenshot [0-9]*.[0-9]', tmp):
            return True
        else:
            return False
        pass
