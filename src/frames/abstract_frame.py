import tkinter as tk
from abc import ABC, abstractmethod


class AbstractFrame(ABC, tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self._create_widgets()

    @abstractmethod
    def _create_widgets(self) -> None:
        pass
