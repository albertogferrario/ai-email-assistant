import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, Dict, List, Optional, Type

from src.exceptions import NextCommandAborted
from src.frames import AbstractFrame


class NavigationView(AbstractFrame):
    __parent: Optional[Any] = None
    __frames: Dict[Type[AbstractFrame], Optional[AbstractFrame]] = {}
    __on_next_frame_pressed: List[Optional[Callable[[], None]]] = []
    __current_frame_index: Optional[int] = None
    __back_button: Optional[tk.Button] = None
    __next_button: Optional[tk.Button] = None

    def __init__(
        self,
        parent,
        frames_types: List[Type[AbstractFrame]],
        on_next_frame_pressed: List[Optional[Callable[[], None]]]
    ):
        if len(on_next_frame_pressed) != len(frames_types) - 1:
            raise ValueError  # fixme: message

        self.__parent = parent
        self.__frames = dict.fromkeys(frames_types, None)
        self.__on_next_frame_pressed = on_next_frame_pressed

        super().__init__(parent)

        self.pack()

    def get_frame(self, index: int) -> AbstractFrame:
        return list(self.__frames.values())[index]

    def _create_widgets(self) -> None:
        for frame_type in self.__frames:
            frame = frame_type(self)
            frame.grid(row=0, column=0, columnspan=2, sticky='nsew')

            self.__frames[frame_type] = frame

        self.__back_button = ttk.Button(self, text="Back", command=lambda: self.__back_button_command())
        self.__back_button.grid(row=1, column=0, padx=10, pady=10)

        self.__next_button = ttk.Button(self, text="Next", command=lambda: self.__next_button_command())
        self.__next_button.grid(row=1, column=1, padx=10, pady=10)

        self.__set_current_frame(0)

        super()._create_widgets()

    def __disable_all(self) -> None:
        self.__disable_back_button()
        self.__disable_next_button()
        self.__disable_frames()

    def __enable_all(self) -> None:
        self.__disable_all()

        if self.__current_frame_index > 0:
            self.__enable_back_button()

        if self.__current_frame_index < len(self.__frames):
            self.__enable_next_button()

        self.__enable_frames()

    def __disable_frames(self) -> None:
        map(lambda frame: frame.state(['disabled']), self.__frames.values())

    def __enable_frames(self) -> None:
        map(lambda frame: frame.state(['!disabled']), self.__frames.values())

    def __disable_back_button(self) -> None:
        self.__back_button.state(['disabled'])  # fixme: to be tested

    def __enable_back_button(self) -> None:
        self.__back_button.state(['!disabled'])  # fixme: to be tested

    def __disable_next_button(self) -> None:
        self.__next_button.state(['disabled'])  # fixme: to be tested

    def __enable_next_button(self) -> None:
        self.__next_button.state(['!disabled'])  # fixme: to be tested

    def __back_button_command(self) -> None:
        if self.__current_frame_index == 0:
            raise ValueError  # fixme: message

        self.__set_current_frame(self.__current_frame_index - 1)

    def __next_button_command(self) -> None:
        if self.__current_frame_index == len(self.__frames):
            raise ValueError  # fixme: message

        self.__disable_all()

        self.__parent.update()

        try:
            self.__on_next_frame_pressed[self.__current_frame_index]()

        except NextCommandAborted:
            pass

        else:
            self.__set_current_frame(self.__current_frame_index + 1)

        self.__enable_all()

    def __show_frame(self, index: int) -> None:
        self.get_frame(index).tkraise()

    def __set_current_frame(self, index: int) -> None:
        self.__current_frame_index = index

        self.__enable_all()

        self.__show_frame(self.__current_frame_index)
