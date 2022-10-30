import os
import platform


class yandexAPI:
    app_id = None
    app_password = None
    url = None

    def __init__(self):
        self.uname_os = os.getlogin()
        self.system = platform.system()
        self.app_id = 'db24be316a0b48a39b9acc58372f5c3b'
        self.app_password = '434e1aa7a2634c30badb19f4b5c63aff'
        self.url = 'https://oauth.yandex.ru/authorize?response_type=code&client_id=' + \
                   self.app_id + '&device_name=' + self.system
        self.folder = 'pyshooter'
        self.separator = '%2F'

yandex = yandexAPI()
