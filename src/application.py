import tkinter as tk

from config import WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH
from src.frames import InputFrame, OutputFrame, ProductsFrame
from src.views import NavigationView


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        main_frame = NavigationView(self, [InputFrame, ProductsFrame, OutputFrame])
        main_frame.pack()
