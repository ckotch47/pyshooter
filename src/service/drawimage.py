import configparser
import os
import tkinter as tk

from PIL import ImageGrab

from src.module.position import pos
from src.module.yandex.login import login
from src.module.yandex.upload import upload

import src.gui.settings as settings
import src.gui.about as about

import src.locale as lc
class canvasService:
    paint = 'rectangle'
    color = 'red'
    width = 1
    cnf = {
        'arrowshape': (10, 20, 10)
    }
    menu = None

    def __init__(self, tk):
        self._root = tk
        self.image_path = None
        self.canvas = None
        self.photo = None
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.paint = self.config['DEFAULT']['brush']
        self.width = self.config['DEFAULT']['width']
        self.color = self.config['DEFAULT']['color']

    def canvasSettings(self, image, MainWindow, width, height):
        self.image_path = image
        self.photo = tk.PhotoImage(file=image)
        self.canvas = tk.Canvas(MainWindow, width=str(width), height=str(height), borderwidth=0,
                                border=0, relief='ridge', highlightthickness=0, )
        self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.pack()

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)

    def my_pass(self):
        pass

    def popup(self, event):
        self.menu.post(event.x_root, event.y_root)

    def brushSelect(self, option=None):
        self.paint = option
        self.config['DEFAULT']['brush'] = self.paint
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def colorSelect(self, option=None):
        self.color = option
        self.config['DEFAULT']['color'] = self.color
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def widthSelect(self, option):
        self.width = option
        self.config['DEFAULT']['width'] = str(self.width)
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def menuSettings(self):
        self.menu = tk.Menu(tearoff=0)
        brush_menu = tk.Menu(self.menu, tearoff=0)
        brush_menu.add_radiobutton(label=lc.menu.line, command=lambda: self.brushSelect('line'))
        brush_menu.add_radiobutton(label=lc.menu.arrow, command=lambda: self.brushSelect('arrow'))
        brush_menu.add_radiobutton(label=lc.menu.rectangle, command=lambda: self.brushSelect('rectangle'))
        self.menu.add_cascade(label=lc.menu.brush, menu=brush_menu)

        color_menu = tk.Menu(self.menu, tearoff=0)
        color_menu.add_radiobutton(label=lc.menu.red, command=lambda: self.colorSelect('red'))
        color_menu.add_radiobutton(label=lc.menu.green, command=lambda: self.colorSelect('green'))
        color_menu.add_radiobutton(label=lc.menu.purple, command=lambda: self.colorSelect('purple'))
        self.menu.add_cascade(label=lc.menu.color, menu=color_menu)

        width_menu = tk.Menu(self.menu, tearoff=0)
        width_menu.add_radiobutton(label=f'1', command=lambda: self.widthSelect(1))
        width_menu.add_radiobutton(label=f'2', command=lambda: self.widthSelect(2))
        width_menu.add_radiobutton(label=f'3', command=lambda: self.widthSelect(3))
        width_menu.add_radiobutton(label=f'4', command=lambda: self.widthSelect(4))
        width_menu.add_radiobutton(label=f'5', command=lambda: self.widthSelect(5))
        width_menu.add_radiobutton(label=f'6', command=lambda: self.widthSelect(6))
        width_menu.add_radiobutton(label=f'7', command=lambda: self.widthSelect(7))
        width_menu.add_radiobutton(label=f'8', command=lambda: self.widthSelect(8))
        width_menu.add_radiobutton(label=f'9', command=lambda: self.widthSelect(9))
        width_menu.add_radiobutton(label=f'10', command=lambda: self.widthSelect(10))
        self.menu.add_cascade(label=lc.menu.width, menu=width_menu)

        self.menu.add_separator()
        self.menu.add_command(label=lc.menu.copy, command=self.copy)
        self.menu.add_command(label=lc.menu.save, command=self.save)
        self.menu.add_command(label=lc.menu.upload, command=self.upload)
        self.menu.add_separator()

        setting_menu = tk.Menu(self.menu, tearoff=0)
        setting_menu.add_command(label=lc.menu.performance, command=settings.show)
        setting_menu.add_command(label=lc.menu.about, command=about.show)
        self.menu.add_cascade(label=lc.menu.settings, menu=setting_menu)
        self.menu.add_separator()

        self.menu.add_command(label=lc.menu.none, command=self.menu.grab_release)
        self.menu.add_command(label=lc.menu.exit, command=self.on_closing)

    @staticmethod
    def on_closing():
        exit(0)

    def copy(self, is_exit=True):
        widget = self.canvas
        ImageGrab.grab((
            widget.winfo_rootx(),
            widget.winfo_rooty(),
            widget.winfo_rootx() + widget.winfo_width(),
            widget.winfo_rooty() + widget.winfo_height()
        )).copy()
        if self.config['DEFAULT']['delete_file'] == 'yes':
            os.remove(self.image_path)

        if is_exit is True:
            exit(0)

    def save(self, is_exit=True):
        widget = self.canvas
        ImageGrab.grab((
            widget.winfo_rootx(),
            widget.winfo_rooty(),
            widget.winfo_rootx() + widget.winfo_width(),
            widget.winfo_rooty() + widget.winfo_height()
        )).save(self.image_path)

        if is_exit is True:
            exit(0)

    def upload(self):
        self.menu.grab_release()
        if not login.isLogin() is None:
            login.show()
        self.save(is_exit=False)
        self._root.destroy()
        temp_del = True
        if self.config['DEFAULT']['delete_file'] == 'no':
            temp_del = False
        elif self.config['DEFAULT']['delete_file'] == 'yes':
            temp_del = True

        upload.loadToFolder(filename=self.image_path, is_delete=temp_del)
        exit(101)

    def on_button_press(self, event):
        pos.x1 = event.x
        pos.y1 = event.y
        if self.paint == 'rectangle':
            pos.paint = self.canvas.create_rectangle(pos.x1, pos.y1, pos.x1 + 1, pos.y1 + 1, outline=self.color,
                                                     width=self.width)
        if self.paint == 'line':
            pos.paint = self.canvas.create_line(pos.x1, pos.y1, pos.x1 + 1, pos.y1 + 1, fill=self.color,
                                                width=self.width)
        if self.paint == 'arrow':
            pos.paint = self.canvas.create_line(pos.x1, pos.y1, pos.x1 + 1, pos.y1 + 1, fill=self.color,
                                                arrow=tk.LAST, width=self.width,
                                                arrowshape=self.cnf['arrowshape'])

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        self.canvas.coords(pos.paint, pos.x1, pos.y1, curX, curY)
