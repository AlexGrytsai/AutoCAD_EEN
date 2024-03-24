import tkinter as tk
from tkinter import ttk


class App(ttk.Frame):
    def __init__(self, parent=None) -> None:
        ttk.Frame.__init__(self)


# root = tk.Tk()
# root.tk.call("source", "app/files/Theme/azure.tcl")
# root.tk.call("set_theme", "light")
# icon = tk.PhotoImage(file='app/files/Theme/auto-cad.png')
# root.iconphoto(False, icon)
# root.title("AutoCAD EEN")
# root.geometry("200x200+1000+200")
# root.minsize(280, 500)
#
# root.mainloop()
