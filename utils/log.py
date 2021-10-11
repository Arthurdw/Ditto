# Copyright Arthurdw 2021-present
# Full MIT License can be found in `LICENSE` at the project root.

from enum import IntEnum
from typing import Any, Tuple, Dict

from colorama import Fore, Style


class LogLevel(IntEnum):
    DEBUG = 4
    INFO = 3
    WARN = 2
    ERROR = 1


class Logging:
    __level: LogLevel = LogLevel.INFO
    __colors: Dict[LogLevel, str] = {
        LogLevel.DEBUG: Fore.BLUE,
        LogLevel.INFO: Fore.CYAN,
        LogLevel.WARN: Fore.YELLOW,
        LogLevel.ERROR: Fore.RED
    }

    @staticmethod
    def set_level(level: LogLevel):
        Logging.__level = level

    @staticmethod
    def __print(level: LogLevel, args: Tuple[Any]):
        if level >= Logging.__level:
            print(
                Logging.__colors[level],
                " ".join(tuple(map(lambda x: str(x), args))),
                Style.RESET_ALL,
                sep=""
            )

    @staticmethod
    def info(*args: Any):
        Logging.__print(LogLevel.INFO, args)

    @staticmethod
    def warn(*args: Any):
        Logging.__print(LogLevel.WARN, args)

    @staticmethod
    def error(*args: Any):
        Logging.__print(LogLevel.ERROR, args)
