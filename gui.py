import tkinter
from tkinter import *
import os
#pyinstaller --onefile gui.py --hidden-import='PIL._tkinter_finder'

import pyautogui as gui
from PIL import ImageTk
from drawimage import drawImage
from position import pos


class MyGUI:
    def __init__(self):
        self.shoot = None
        self.menu = None
        self.canvas = None
        self.__mainWindow = None
        self.start = True

    def show(self):
        self.mainWindowSettings()
        self.menuSettings()
        self.createCanvas()
        self.canvasSettings()
        mainloop()

    def createCanvas(self):
        self.canvas = tkinter.Canvas(self.__mainWindow, width=str(gui.size().width), height=str(gui.size().height + 5),
                                     bg="red")
        img = gui.screenshot()

        self.shoot = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor='nw', image=self.shoot)
        self.canvas.pack(expand=True)

    def mainWindowSettings(self):
        self.__mainWindow = Tk()
        self.__mainWindow.geometry(str(gui.size().width) + "x" + str(gui.size().height))
        self.__mainWindow.attributes('-alpha', 1)
        self.__mainWindow.attributes('-type', 'normal')
        self.__mainWindow.overrideredirect(True)
        self.__mainWindow.bind("<Button-3>", self.popup)
        self.__mainWindow.protocol("WM_DELETE_WINDOW", self.on_closing)



    def menuSettings(self):
        self.menu = Menu(tearoff=0)
        self.menu.add_command(label="none", command=self.menu.grab_release)
        self.menu.add_command(label="exit", command=self.on_closing)

    def canvasSettings(self):
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def popup(self, event):
        self.menu.post(event.x_root, event.y_root)

    def on_button_press(self, event):
        pos.x1 = gui.position().x
        pos.y1 = gui.position().y
        pos.rect = self.canvas.create_rectangle(pos.x1, pos.y1, pos.x1 + 1, pos.y1 + 1)

    def on_move_press(self, event):
        curX, curY = (gui.position().x, gui.position().y)
        self.canvas.coords(pos.rect, pos.x1, pos.y1, curX, curY)

    def on_button_release(self, event):
        pos.x2 = gui.position().x
        pos.y2 = gui.position().y
        pos.MySwapAll()
        # name = 'temp/shoot_0.png'
        photos = gui.screenshot(region=(pos.x1, pos.y1, pos.x2 - pos.x1, pos.y2 - pos.y1))
        # os.remove('temp/temp.png')
        self.__mainWindow.destroy()
        drawImage.show(width=pos.x2 - pos.x1, height=pos.y2 - pos.y1, image=photos)


    def on_closing(self):
        # os.remove('temp/temp.png')
        self.__mainWindow.destroy()


myGUI = MyGUI()
myGUI.show()
