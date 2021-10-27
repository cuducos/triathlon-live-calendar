import logging
from dataclasses import dataclass
from typing import Iterable, Union

from typer import echo


@dataclass
class Logger:
    use_typer_echo: bool = False

    def info(self, text: Union[str, Iterable[str]]) -> None:
        if not isinstance(text, str):
            text = "\n".join(text)

        if self.use_typer_echo:
            echo(text)
        else:
            logging.info(text)
