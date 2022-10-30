from configparser import ConfigParser
from tkinter import *
from tkinter import filedialog

from src.locale import app_locale
from src.module.errorsmsg import *
import src.locale as lc
config = ConfigParser()


def show(main_window=False):
    if main_window is True:
        _root = Tk()
    else:
        _root = Toplevel()

    _root.geometry("500x200")

    _root.wm_title(lc.performance.title)

    text_info = Frame(_root)
    text_info.pack(expand=1, padx=20, pady=10, fill='x', anchor='nw')
    Label(text_info, text=lc.performance.text).pack(side='top')


    frame_folder = Frame(_root)
    frame_folder.pack(expand=1, padx=20, pady=0, fill='x', anchor='n')
    Label(frame_folder, text=lc.performance.labelFolder).pack(side='left')
    Button(frame_folder, text=lc.performance.chose, command=select_folder).pack(side='right')

    config.read('config.ini')
    temp_locale = config.get('DEFAULT', 'locale')

    locale_var = StringVar()
    if temp_locale in app_locale:
        locale_var.set(temp_locale)
    else:
        locale_var.set(app_locale[0])

    config.read('config.ini')
    temp_delete = False
    if config.get('DEFAULT', 'delete_file') == 'yes':
        temp_delete = True
    var = BooleanVar()
    var.set(temp_delete)

    frame_delete_shoot = Frame(_root)
    frame_delete_shoot.pack(expand=1, padx=20, pady=0, fill='x', anchor='n')
    Label(frame_delete_shoot, text=lc.performance.labelDelete).pack(side='left')
    Checkbutton(frame_delete_shoot, variable=var, onvalue=True, offvalue=False, command=lambda: select_delete(var)).pack(side='right')

    # Create Dropdown menu
    frame_locale = Frame(_root)
    frame_locale.pack(expand=1, padx=20, pady=0, fill='x', anchor='n')
    Label(frame_locale, text=lc.performance.labelLocale).pack(side='left')
    OptionMenu(frame_locale, locale_var, *app_locale, command=select_locale).pack(side='right')

    _root.mainloop()


def select_locale(event):
    if event in app_locale:
        config.read('config.ini')
        config['DEFAULT']['locale'] = event
        config.write(open('config.ini', 'w'))


def select_folder():
    try:
        folder_selected = filedialog.askdirectory() + '/'
        config.read('config.ini')
        config['DEFAULT']['path'] = folder_selected
        config.write(open('config.ini', 'w'))
    except TypeError:
        folder_dont_use()


def select_delete(var):
    delete_shoot = 'yes'
    if var.get() is False:
        delete_shoot = 'no'

    config.read('config.ini')
    config['DEFAULT']['delete_file'] = delete_shoot
    config.write(open('config.ini', 'w'))
