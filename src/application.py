import tkinter as tk

from src.frames import InputFrame, OutputFrame, ProductsFrame
from src.views import NavigationView


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("800x600")  # fixme: configurable
        self.title("AI Email Assistant")  # fixme: configurable

        main_frame = NavigationView(self, [InputFrame, ProductsFrame, OutputFrame])
        main_frame.pack()
