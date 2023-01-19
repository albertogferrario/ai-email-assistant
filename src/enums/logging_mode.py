from enum import Enum
from typing import Set


class LoggingMode(Enum):
    value: str

    STDOUT = 'stdout'
    FILE = 'file'

    @classmethod
    def get_values(cls) -> Set[str]:
        return {v.value for v in list(cls)}
