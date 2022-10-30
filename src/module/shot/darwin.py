import configparser
import subprocess
from datetime import datetime


class screenshoot:
    config = configparser.ConfigParser()
    config.read('config.ini')
    path = config['DEFAULT']['path']
    name = ''

    def shoot(self):
        self.name = str(datetime.now()).replace('-', '_').replace(' ', '_').replace(':', '_').split('.')[0]
        subprocess.run(f'screencapture -i {self.path}/{self.name}.png', shell=True,
                       stdout=subprocess.PIPE)

        temp = f'{self.path}/{self.name}.png'
        return temp
