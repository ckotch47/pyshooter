from tkinter import Toplevel, Frame, Label
import src.locale as lc


def show():
    __root = Toplevel()
    __root.geometry("600x200")
    __root.wm_title(lc.about.title)
    frame = Frame(__root)
    label = Label(frame, text=lc.about.text)
    label.pack(pady=20)

    label = Label(frame, text='https://github.com/ckotch47/pyshooter')
    label.pack(pady=20)

    frame.pack(expand=1, fill='both')
