import os
import time
import tkinter
from tkinter import HORIZONTAL
from tkinter.ttk import Progressbar
import requests
import pyperclip
from src.module.yandex.yandex import yandex
from src.module.yandex.login import login
from tkinter import messagebox
from tkinter import Tk


class Upload:
    def __init__(self):
        self.loader = None
        self.entry = None
        self.progress = None
        self.__mainWindow = None
        self.pathIMG = 'shoot.png'
        self.folder = yandex.folder
        self.link = ''

    def checkFolder(self):
        login.isLogin()
        res = requests.get(url='https://cloud-api.yandex.net/v1/disk/resources?path=' + yandex.folder,
                           headers={"Authorization": "OAuth " + str(login.access_token)})
        if res.status_code == 404:
            return self.createFolder()
        else:
            return False

    def createFolder(self):
        login.isLogin()
        res = requests.put(url='https://cloud-api.yandex.net/v1/disk/resources?path=' + yandex.folder,
                           headers={"Authorization": "OAuth " + str(login.access_token)})
        if res.status_code == 201:
            return True
        else:
            return False

    def getLinkToUpload(self, name):
        self.checkFolder()
        login.isLogin()
        res = requests.get(url='https://cloud-api.yandex.net/v1/disk/resources/upload?path=' + yandex.separator
                               + yandex.folder + yandex.separator + name,
                           headers={"Authorization": "OAuth " + str(login.access_token)})
        if res.status_code != 409:
            self.link = res.json()['href']
            return self.link
        else:
            return 'File is exist'

    def loadToFolder(self, filename, is_delete=False):
        name = filename.split('/')[-1]
        login.isLogin()
        self.checkFolder()
        link = self.getLinkToUpload(name=name)
        with open(filename, 'rb') as file:
            try:
                res = requests.put(url=link, files={'file': file})
                time.sleep(.5)
                if is_delete is True:
                    os.remove(filename)
                return self.makeFilePublish(name)
            except KeyError:
                return False

    def makeFilePublish(self, name):
        login.isLogin()
        res = requests.put(url='https://cloud-api.yandex.net/v1/disk/resources/publish?path='
                               + yandex.separator + yandex.folder + yandex.separator + name,
                           headers={"Authorization": "OAuth " + str(login.access_token)})

        if res.status_code == 200:
            res = requests.get(url='https://cloud-api.yandex.net/v1/disk/resources?path='
                                   + yandex.separator + yandex.folder + yandex.separator + name,
                               headers={"Authorization": "OAuth " + str(login.access_token)})

            self.showMassage(res.json()['public_url'])
            return res.json()['public_url']
        else:
            return False

    def GUILoader(self):
        self.__mainWindow = Tk()
        self.progress = Progressbar(self.__mainWindow, orient=HORIZONTAL,
                                    length=100, mode='determinate')
        self.progress.pack(pady=10, padx=10)
        self.bar(25, '+')
        tkinter.mainloop()

    def bar(self, value, arrow):
        self.progress['value'] = value
        self.__mainWindow.update_idletasks()
        time.sleep(.3)
        if arrow == '+':
            if value >= 100:
                arrow = '-'
            value += 25
        else:
            if value <= 0:
                arrow = '+'
            value -= 25
        self.bar(value, arrow)

    def showMassage(self, msg):
        self.__mainWindow = tkinter.Tk()
        try:
            pyperclip.copy(msg)  # linux use xclip
            label = tkinter.Label(self.__mainWindow, text='Link copied into clipboard')
            label.pack(padx=10, pady=10)
        except:
            self.entry = tkinter.Entry(self.__mainWindow, width=110)
            self.entry.insert(0, msg)
            self.entry.pack(pady=5, padx=5, side='left')

            btn = tkinter.Button(self.__mainWindow, text='copy', command=self.copy)
            btn.pack(pady=5, padx=5, side='right')
        finally:
            tkinter.mainloop()

    def copy(self):
        try:
            pyperclip.copy(self.entry.get())
        except:
            messagebox.showerror(title='error', message='system not supported', )


upload = Upload()
