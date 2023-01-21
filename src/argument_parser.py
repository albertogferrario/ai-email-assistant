import argparse

from src.enums import LoggingMode


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__()

        self.__logging()
        self.__window()
        self.__openai()

    def __logging(self):
        group = self.add_argument_group('logging')

        group.add_argument(
            '--logging-level',
            choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'],
            default='INFO'
        )
        group.add_argument('--logging-mode', choices=list(LoggingMode.get_values()))
        group.add_argument('--logging-path')
        group.add_argument('--logging-format')

    def __window(self):
        group = self.add_argument_group('window')

        group.add_argument('--window-title')

    def __openai(self):
        group = self.add_argument_group('openai')

        group.add_argument('--openai-api-key')
