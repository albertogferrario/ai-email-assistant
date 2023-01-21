from tkinter import ttk
from typing import List, Tuple

from .abstract_frame import AbstractFrame
from ..fonts import LARGE_FONT


class SecondFrame(AbstractFrame):
    __products: List[Tuple[str, int]] = []
    __price_entries: List[ttk.Entry] = []

    def __init__(self, parent):
        super().__init__(parent)

    def set_products(self, products: List[Tuple[str, int]]) -> None:
        self.__products = products
        self.__create_products_widgets()

    def get_products(self) -> List[Tuple[str, int, float]]:
        return [
            (name, quantity, self.__get_price(idx)) for idx, (name, quantity) in enumerate(self.__products)
        ]

    def _create_widgets(self) -> None:
        label = ttk.Label(self, font=LARGE_FONT, text="Detected products")
        label.grid(row=0, column=1, padx=10, pady=10)

    def __create_products_widgets(self) -> None:
        label = ttk.Label(self, text="Nome")
        label.grid(row=1, column=0, padx=10, pady=10)

        label = ttk.Label(self, text="Quantità")
        label.grid(row=1, column=1, padx=10, pady=10)

        label = ttk.Label(self, text="Prezzo")
        label.grid(row=1, column=2, padx=10, pady=10)

        row_offset = 2

        for idx, (product_name, product_quantity) in enumerate(self.__products):
            label = ttk.Label(self, text=product_name)
            label.grid(row=idx + row_offset, column=0, padx=10, pady=10)

            label = ttk.Label(self, text=str(product_quantity))
            label.grid(row=idx + row_offset, column=1, padx=10, pady=10)

            entry = ttk.Entry(self)
            entry.grid(row=idx + row_offset, column=2, padx=10, pady=10)
            self.__price_entries.append(entry)

    def __get_price(self, index: int) -> float:
        return float(self.__price_entries[index].get())
