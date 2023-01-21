from argparse import Namespace
from configparser import ConfigParser
from logging import getLevelName
from os.path import exists, join
from pathlib import Path
from tkinter.messagebox import showerror
from typing import Any, Optional, Tuple, Type, Union

from src import ArgumentParser
from src.enums import LoggingMode

_INI_FILE_PATH = join(Path(__file__).parent.absolute(), '.ini')

_config: Optional[ConfigParser] = None
_args: Optional[Namespace] = None

if exists(_INI_FILE_PATH):
    _config = ConfigParser()
    _config.read(_INI_FILE_PATH)

_argument_parser = ArgumentParser()
_args = _argument_parser.parse_args()


def _get_config(
    ini_name: Tuple[str, str],
    arg_name: str,
    type_: Type[Union[str, int, float, bool]] = str,
    fallback: Optional[Any] = None,
) -> Union[str, int, float, bool]:
    if not _config:
        val = getattr(_args, arg_name)

        if val is None:
            return fallback

        assert isinstance(val, type_)

        return val

    getters = {
        str: _config.get,
        int: _config.getint,
        float: _config.getfloat,
        bool: _config.getboolean,
    }

    return getters[type_](*ini_name, fallback=fallback)


# ----------------------------------------------------------------------------------------------------------------------
# LOGGING
# ----------------------------------------------------------------------------------------------------------------------
LOGGING_MODE: LoggingMode = LoggingMode(_get_config(('LOGGING', 'MODE'), 'logging_mode',
                                                    fallback=LoggingMode.STDOUT.value))
LOGGING_LEVEL: int = getLevelName(_get_config(('LOGGING', 'LEVEL'), 'logging_level', fallback='INFO'))
LOGGING_PATH: str = _get_config(('LOGGING', 'PATH'), 'logging_path', fallback="")
LOGGING_FORMAT: Optional[str] = _get_config(('LOGGING', 'FORMAT'), 'logging_format')

# ----------------------------------------------------------------------------------------------------------------------
# WINDOW
# ----------------------------------------------------------------------------------------------------------------------
WINDOW_TITLE: str = _get_config(('WINDOW', 'TITLE'), 'window_title', fallback='APP')

# ----------------------------------------------------------------------------------------------------------------------
# OPENAI
# ----------------------------------------------------------------------------------------------------------------------
OPENAI_API_KEY: Optional[str] = _get_config(('OPENAI', 'API_KEY'), 'openai_api_key')
OPENAI_COMPLETION_MAX_TOKENS: int = _get_config(
    ('OPENAI', 'COMPLETION_MAX_TOKENS'), 'openai_completion_max_tokens', fallback=200
)

if OPENAI_API_KEY is None:
    showerror("Errore", "Errore di configurazione. Chiave API per OpenAI non rilevata.")

    raise ValueError  # fixme: message
