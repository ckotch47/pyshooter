from tkinter import messagebox
import src.locale as lc


def dont_define_platform():
    messagebox.showwarning(lc.msgbox.definePlatform['title'], lc.msgbox.definePlatform['text'])


def went_wrong():
    messagebox.showwarning(lc.msgbox.wentWrong['title'], lc.msgbox.wentWrong['title'])


def install_gnome_screenshoot():
    messagebox.showerror(lc.msgbox.installGnomeScreen['title'], lc.msgbox.installGnomeScreen['text'])


def folder_dont_use():
    messagebox.showerror(lc.msgbox.folderDontUse['title'], lc.msgbox.folderDontUse['text'])


def select_folder():
    messagebox.showerror(lc.msgbox.selectFolder['title'], lc.msgbox.selectFolder['text'])
