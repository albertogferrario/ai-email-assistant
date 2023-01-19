import tkinter as tk
from typing import Optional

from .abstract_frame import AbstractFrame


class InputFrame(AbstractFrame):
    __email_text: Optional[tk.Text] = None

    def _create_widgets(self) -> None:
        self.__email_text = tk.Text(self)
        self.__email_text.grid(row=0, column=0, padx=10, pady=10)
