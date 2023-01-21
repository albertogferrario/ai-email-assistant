import tkinter as tk
from tkinter import END, ttk
from typing import Optional

from .abstract_frame import AbstractFrame
from ..fonts import LARGE_FONT


class ThirdFrame(AbstractFrame):
    __quotation_text: Optional[tk.Text] = None

    def set_quotation_text(self, text: str) -> None:
        self.__quotation_text.delete(1.0, END)
        self.__quotation_text.insert(END, text)

    def _create_widgets(self) -> None:
        label = ttk.Label(self, font=LARGE_FONT, text="Generated quotation")
        label.grid(row=0, column=0, padx=10, pady=10)

        self.__quotation_text = tk.Text(self)
        self.__quotation_text.grid(row=1, column=0, padx=10, pady=10)
