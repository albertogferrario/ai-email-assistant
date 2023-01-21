import json
import logging
import tkinter as tk
from json import JSONDecodeError
from tkinter.commondialog import Dialog
from tkinter.messagebox import showerror
from typing import List, Optional, Tuple

import openai

import config
from config import WINDOW_TITLE
from src.exceptions import NextCommandAborted
from src.frames import FirstFrame, SecondFrame, ThirdFrame
from src.views import NavigationView

openai.api_key = config.OPENAI_API_KEY


class Application(tk.Tk):
    __navigation_view: Optional[NavigationView] = None
    __products: Optional[List[Tuple[str, int]]]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(WINDOW_TITLE)

        self.__navigation_view = NavigationView(
            self,
            [FirstFrame, SecondFrame, ThirdFrame],
            [self.on_first_to_second, self.on_second_to_third]
        )
        self.__navigation_view.pack()

    def on_first_to_second(self) -> None:
        first_frame: FirstFrame = self.__navigation_view.get_frame(0)

        email_text = first_frame.get_email_text()

        if not self.__detect_quotation_request_from_text(email_text):
            showerror("Errore", "Non è stata rilevata alcuna richiesta di preventivo.")

            raise NextCommandAborted

        try:
            self.__products = self.__detect_products_from_text(email_text)

        except ValueError:
            showerror("Errore", "Errore durante il caricamento della risposta di OpenAI, riprovare.")

            raise NextCommandAborted


        second_frame: SecondFrame = self.__navigation_view.get_frame(1)
        second_frame.set_products(self.__products)

    def on_second_to_third(self) -> None:
        second_frame: SecondFrame = self.__navigation_view.get_frame(1)
        third_frame: ThirdFrame = self.__navigation_view.get_frame(2)

        try:
            products = second_frame.get_products()

        except ValueError:
            showerror("Errore", "Errore durante la lettura dei campi, verificare i valori impostati e riprovare.")

            raise NextCommandAborted

        third_frame.set_quotation_text(self.__generate_quotation_text(products))

    @staticmethod
    def __detect_quotation_request_from_text(text: str) -> bool:
        if len(text) == 0:
            return False

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Is the following text a request for a quote or is a request for the price of some products: {text}"
                   f"? Please answer only 'yes' o 'no'.",  # fixme: migliorare
            max_tokens=config.OPENAI_COMPLETION_MAX_TOKENS,
        )

        return response['choices'][0]['text'].strip().lower().find("yes") >= 0

    @staticmethod
    def __detect_products_from_text(text: str) -> List[Tuple[str, int]]:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Puoi identificare ed elencare i prodotti e la quantità per cui viene richiesto il preventivo in "
                   f"questa richiesta di preventivo: {text}? Per favore rispondi solo elencando i prodotti e i "
                   f"rispetivi prezzi nel seguente formato: '[[\"nome convertito al singolare\",quantità],"
                   f"[\"nome convertito al singolare\",quantità]'.",  # fixme: migliorare
            max_tokens=config.OPENAI_COMPLETION_MAX_TOKENS,
        )

        response = response['choices'][0]['text'].strip().lower().replace(".", "").replace("'", "\"")

        if response.find(": ") >= 0:
            response = response.split(": ")[1]

        if response.find("[[") == -1:
            response = f"[{response}]"

        try:
            response = json.loads(response)

        except JSONDecodeError:
            raise ValueError  # fixme: has to be a custom exception class

        try:
            products = [(item[0], item[1]) for item in response]

        except:
            raise ValueError  # fixme: has to be a custom exception class

        return products

    @staticmethod
    def __generate_quotation_text(products: List[Tuple[str, int, float]]) -> str:
        prompt = "Can you generate a quotation formal email in italian language for this products:\n"

        for idx, (name, quantity, price) in enumerate(products):
            prompt += f"product {idx}: name={name}, quantity={quantity}, unit price={price}\n"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,  # fixme: migliorare
            max_tokens=config.OPENAI_COMPLETION_MAX_TOKENS,
        )

        return response['choices'][0]['text']
