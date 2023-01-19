from logging import basicConfig, getLevelName
from sys import stdout

from config import LOGGING_FORMAT, LOGGING_LEVEL, LOGGING_MODE, LOGGING_PATH
from src import Application
from src.enums import LoggingMode


def init_logging() -> None:
    kwargs = {
        'level': LOGGING_LEVEL,
        'format': LOGGING_FORMAT,
    }

    if LOGGING_MODE == LoggingMode.STDOUT:
        kwargs['stream'] = stdout

    else:
        kwargs['filename'] = f'{LOGGING_PATH}/{getLevelName(LOGGING_LEVEL)}.log'

    basicConfig(**kwargs)


def init_application() -> None:
    application = Application()
    application.mainloop()
