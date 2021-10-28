from dataclasses import dataclass
from functools import cached_property, wraps
from logging import INFO, Formatter, StreamHandler, getLogger
from sys import stdout
from typing import Iterable, Union


def multiline(func):
    @wraps(func)
    def normalized(self, text: Union[str, Iterable[str]]):
        if not isinstance(text, str):
            text = "\n".join(text)

        return func(self, text)

    return normalized


@dataclass
class Logger:
    log_level: int = INFO

    def __post_init__(self):
        self.logger = getLogger()
        self.logger.setLevel(self.log_level)
        self.logger.addHandler(self.handler)

    @cached_property
    def handler(self):
        handler = StreamHandler(stdout)
        handler.setLevel(self.log_level)
        handler.setFormatter(
            Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        return handler

    @multiline
    def critical(self, text):
        self.logger.critical(text)

    @multiline
    def debug(self, text):
        self.logger.debug(text)

    @multiline
    def error(self, text):
        self.logger.error(text)

    @multiline
    def info(self, text):
        self.logger.info(text)

    @multiline
    def warning(self, text):
        self.logger.warning(text)
