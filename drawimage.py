import tkinter as tk
from time import sleep
from PIL import ImageGrab
from PIL.ImageTk import PhotoImage
from position import pos


class myGUI:
    def __init__(self):
        self.height = None
        self.width = None
        self.photo = None
        self.canvas = None
        self.__MainWindow = None
        self.menu = None
        self.paint = 'rectangle'
        self.cnf = {
            'fill': 'red',
            'width': 5,
            'arrowshape': (10, 20, 10)
        }
        self.image = None

    def popup(self, event):
        self.menu.post(event.x_root, event.y_root)

    @staticmethod
    def on_closing():
        exit(123)

    def getter(self, widget):
        x = self.__MainWindow.winfo_rootx() + widget.winfo_x()
        y = self.__MainWindow.winfo_rooty() + widget.winfo_y()
        x1 = x + widget.winfo_width()
        y1 = y + widget.winfo_height()
        ImageGrab.grab().crop((x, y, x1, y1)).save("shoot.png")

    def saveImage(self):
        self.menu.grab_release()
        sleep(.05)
        self.getter(self.canvas)
        # self.canvas.postscript(file="temp.ps")
        # img = Image.open("temp.ps")
        # img.save("shoot.bmp", format='bmp')
        # os.remove('temp.ps')
        exit(101)

    def radioSelect(self, option=None):
        self.paint = option

    def menuSettings(self):
        self.menu = tk.Menu(tearoff=0)
        self.menu.add_radiobutton(label='line', command=lambda: self.radioSelect('line'))
        self.menu.add_radiobutton(label='arrow', command=lambda: self.radioSelect('arrow'))
        self.menu.add_radiobutton(label='rectangle', command=lambda: self.radioSelect('rectangle'))
        self.menu.add_separator()
        self.menu.add_command(label='save', command=self.saveImage)
        self.menu.add_command(label='upload', command=self.saveImage)
        self.menu.add_separator()
        self.menu.add_command(label="none", command=self.menu.grab_release)
        self.menu.add_command(label="exit", command=self.on_closing)

    def guiSettings(self):
        self.__MainWindow = tk.Tk()
        self.__MainWindow.geometry(str(self.width) + 'x' + str(self.height))
        self.__MainWindow.overrideredirect(False)
        self.__MainWindow.bind("<Button-3>", self.popup)

    def canvasSettings(self):
        self.photo = PhotoImage(self.image)
        self.canvas = tk.Canvas(self.__MainWindow, width=str(self.width), height=str(self.height + 5), bg="gray")
        self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.pack()

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)

    def on_button_press(self, event):
        pos.x1 = event.x
        pos.y1 = event.y
        if self.paint == 'rectangle':
            pos.paint = self.canvas.create_rectangle(pos.x1, pos.y1, pos.x1 + 1, pos.y1 + 1, outline=self.cnf['fill'],
                                                     width=self.cnf['width'])
        if self.paint == 'line':
            pos.paint = self.canvas.create_line(pos.x1, pos.y1, pos.x1 + 1, pos.y1 + 1, fill=self.cnf['fill'],
                                                width=self.cnf['width'])
        if self.paint == 'arrow':
            pos.paint = self.canvas.create_line(pos.x1, pos.y1, pos.x1 + 1, pos.y1 + 1, fill=self.cnf['fill'],
                                                arrow=tk.LAST, width=self.cnf['width'],
                                                arrowshape=self.cnf['arrowshape'])

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        self.canvas.coords(pos.paint, pos.x1, pos.y1, curX, curY)

    def show(self, width=0, height=0, image=None):
        self.image = image
        self.width = width
        self.height = height

        self.guiSettings()
        self.menuSettings()
        self.canvasSettings()

        tk.mainloop()


drawImage = myGUI()
