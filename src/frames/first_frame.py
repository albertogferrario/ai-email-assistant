import tkinter as tk
from tkinter import END, ttk
from typing import Optional

from .abstract_frame import AbstractFrame
from ..fonts import LARGE_FONT


class FirstFrame(AbstractFrame):
    __email_text: Optional[tk.Text] = None

    def get_email_text(self) -> str:
        return self.__email_text.get(1.0, END).strip()

    def _create_widgets(self) -> None:
        label = ttk.Label(self, font=LARGE_FONT, text="Customer email message")
        label.grid(row=0, column=0, padx=10, pady=10)

        self.__email_text = tk.Text(self)
        self.__email_text.grid(row=1, column=0, padx=10, pady=10)
