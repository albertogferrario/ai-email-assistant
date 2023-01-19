import tkinter as tk
from tkinter import ttk
from typing import List, Optional, Type

from src.frames import AbstractFrame


class NavigationView(AbstractFrame):
    __frames: List[AbstractFrame] = []
    __frames_types: List[Type[AbstractFrame]] = []
    __current_frame_index: int = 0
    __back_button: Optional[tk.Button] = None
    __next_button: Optional[tk.Button] = None

    def __init__(self, parent, frames_types: List[Type[AbstractFrame]]):
        self.__frames_types = frames_types

        super().__init__(parent)

        self.pack(side='top', fill='both', expand=True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def disable_back_button(self) -> None:
        pass  # fixme

    def disable_next_button(self) -> None:
        pass  # fixme

    def __hide_back_button(self) -> None:
        pass  # fixme

    def __hide_next_button(self) -> None:
        pass  # fixme

    def __back_button_command(self) -> None:
        if self.__current_frame_index == 0:
            raise ValueError  # fixme: message

        self.__current_frame_index = self.__current_frame_index - 1

        if self.__current_frame_index == 0:
            self.__hide_back_button()

        self.__show_frame(self.__current_frame_index)

    def __next_button_command(self) -> None:
        if self.__current_frame_index == len(self.__frames):
            raise ValueError  # fixme: message

        self.__current_frame_index = self.__current_frame_index + 1

        if self.__current_frame_index == len(self.__frames):
            self.__hide_next_button()

        self.__show_frame(self.__current_frame_index)

    def __show_frame(self, index: int) -> None:
        self.__frames[index].tkraise()

    def _create_widgets(self) -> None:
        for frame_type in self.__frames_types:
            frame = frame_type(self)
            frame.grid(row=0, column=0, sticky='nsew')

            self.__frames.append(frame)

        self.__show_frame(self.__current_frame_index)

        self.__back_button = ttk.Button(self, text="Back", command=lambda: self.__back_button_command())
        self.__back_button.grid(row=0, column=1, padx=10, pady=10)

        self.__next_button = ttk.Button(self, text="Next", command=lambda: self.__next_button_command())
        self.__next_button.grid(row=1, column=1, padx=10, pady=10)

        super()._create_widgets()
