import os
import time
import tkinter
import requests
import pyperclip
from src.module.yandex.yandex import yandex
from src.module.yandex.login import login
from tkinter import messagebox
import src.locale as lc


class Upload:
    def __init__(self):
        self.loader = None
        self.entry = None
        self.progress = None
        self.__mainWindow = None
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

    @staticmethod
    def createFolder():
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
                requests.put(url=link, files={'file': file})
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

    def showMassage(self, msg):
        self.__mainWindow = tkinter.Tk()
        self.__mainWindow.wm_title(lc.uploadYandex.title)
        try:
            pyperclip.copy(msg)  # linux use xclip
            label = tkinter.Label(self.__mainWindow, text=lc.uploadYandex.text_copy_successful)
            label.pack(padx=10, pady=10)
        except:
            self.entry = tkinter.Entry(self.__mainWindow, width=110)
            self.entry.insert(0, msg)
            self.entry.pack(pady=5, padx=5, side='left')

            btn = tkinter.Button(self.__mainWindow, text=lc.uploadYandex.text_btn_copy, command=self.copy)
            btn.pack(pady=5, padx=5, side='right')
        finally:
            tkinter.mainloop()

    def copy(self):
        try:
            pyperclip.copy(self.entry.get())
        except:
            messagebox.showerror(title=lc.msgbox.dontUseClipboard['title'], message=lc.msgbox.dontUseClipboard['text'])


upload = Upload()
