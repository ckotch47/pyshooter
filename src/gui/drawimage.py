import tkinter as tk
from PIL import Image

from src.service.drawimage import canvasService


class CanvasGui:
    def __init__(self):
        self.canvas_service = None
        self.height = None
        self.width = None
        self.photo = None
        self.canvas = None
        self.__MainWindow = None
        self.image = None

    def guiSettings(self):
        self.__MainWindow = tk.Tk()
        self.canvas_service = canvasService(self.__MainWindow)
        self.__MainWindow.wm_title(self.image)
        self.__MainWindow.geometry(str(self.width) + 'x' + str(self.height))
        self.__MainWindow.attributes('-alpha', 1)
        self.__MainWindow.attributes('-type', 'normal')
        self.__MainWindow.resizable(width=False, height=False)
        self.__MainWindow.bind("<Button-3>", self.canvas_service.popup)


    def show(self, image=None):
        self.image = image
        temp = Image.open(self.image)
        self.width = temp.width
        self.height = temp.height

        self.guiSettings()
        self.canvas_service.menuSettings()
        self.canvas_service.canvasSettings(
            self.image,
            self.__MainWindow,
            self.width,
            self.height
        )

        tk.mainloop()


canvas_gui = CanvasGui()
