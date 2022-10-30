from configparser import ConfigParser
from src.locale.app_locale import app_locale

config = ConfigParser()
config.read('config.ini')
this_locale = config.get('DEFAULT', 'locale')

if this_locale == 'ru':
    from src.locale.ru import *
else:
    from src.locale.en import *


