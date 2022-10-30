import configparser
import tkinter
import os.path
import requests
from PIL import Image, ImageTk
import qrcode
from src.module.yandex.yandex import yandex


class Login:
    def __init__(self):
        self.__mainWindow = None
        self.code = None
        self.jwt = None
        self.access_token = None
        self.config = configparser.ConfigParser()
        self.config.read('settings.ini')

    def isLogin(self):
        if self.config['YANDEX']['access_token'] != 'None' and self.config['YANDEX']['jwt'] != 'None':
            self.access_token = self.config['YANDEX']['access_token']
            self.jwt = self.config['YANDEX']['jwt']

            res = requests.get(url='https://cloud-api.yandex.net/v1/disk',
                               headers={"Authorization": "OAuth " + self.access_token})
            if res.status_code == 401:
                return self.refreshJWT()
        else:
            return False

    def refreshJWT(self):
        res = requests.post(url='https://oauth.yandex.ru/token', data={
            'grant_type': 'refresh_token',
            'refresh_token': self.jwt,
            'client_id': yandex.app_id,
            'client_secret': yandex.app_password
        })

        if res.status_code == 401 or res.status_code == 400:
            self.GUI()
        else:
            res = res.json()
            self.config['YANDEX']['access_token'] = res['access_token']
            self.access_token = res['access_token']
            self.jwt = res['refresh_token']
            self.config['YANDEX']['jwt'] = res['refresh_token']
            self.config['YANDEX']['token_type'] = res['token_type']
            with open('settings.ini', 'w') as configfile:
                self.config.write(configfile)
            return True

    @staticmethod
    def generateQR():
        data = yandex.url
        filename = 'temp/qr_code.png'
        img = qrcode.make(data)
        img.save(filename)

    def GUI(self):
        if self.checkCode():
            image = Image.open("temp/qr_code.png")
        else:
            self.generateQR()
            image = Image.open("temp/qr_code.png")

        self.__mainWindow = tkinter.Toplevel()
        # label
        label = tkinter.Label(self.__mainWindow,text='scan qr or open link into browser')
        label.pack(pady=5)

        # image
        canvas = tkinter.Canvas(self.__mainWindow, height=image.height, width=image.width)
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor='nw', image=photo)
        canvas.pack(pady=5)

        # link
        link = tkinter.Entry(self.__mainWindow,width=65)
        link.insert(0, yandex.url)
        link.pack(pady=5)

        label = tkinter.Label(self.__mainWindow, text='past code and go')
        label.pack()

        frame = tkinter.Frame(self.__mainWindow)
        frame.pack(side='bottom', fill='none')

        self.code = tkinter.Entry(frame, width=60)
        self.code.pack(side='left')

        btn = tkinter.Button(frame, text='go', command=self.sendCode)
        btn.pack(side='right')

        tkinter.mainloop()

    def sendCode(self):
        try:
            temp = requests.post(url='https://oauth.yandex.ru/token', data={
                'grant_type': 'authorization_code',
                'code': self.code.get(),
                'client_id': yandex.app_id,
                'client_secret': yandex.app_password
            }).json()
            self.config['YANDEX']['access_token'] = temp['access_token']
            self.access_token = temp['access_token']
            self.jwt = temp['refresh_token']
            self.config['YANDEX']['jwt'] = temp['refresh_token']
            self.config['YANDEX']['token_type'] = temp['token_type']
            with open('settings.ini', 'w') as configfile:
                self.config.write(configfile)
            self.__mainWindow.destroy()
        except:
            print('error')

    @staticmethod
    def checkCode():
        if os.path.isfile('temp/qr_code.png'):
            return True
        else:
            return False

    def show(self):
        if self.isLogin():
            return True
        else:
            self.GUI()


login = Login()

