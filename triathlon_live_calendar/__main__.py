import asyncio
from os import getenv
from pathlib import Path
from typing import Optional

from typer import Typer, Option
from uvicorn import run  # type: ignore

from triathlon_live_calendar.calendar import calendar
from triathlon_live_calendar.logger import Logger


DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 5000
PORT_HELP = "[default: 5000 or PORT from environment variable]"

app = Typer()


def get_port(value: Optional[str]) -> int:
    if value:
        return int(value)

    try:
        return int(getenv("PORT", ""))
    except ValueError:
        return DEFAULT_PORT


@app.command()
def web(
    host: str = DEFAULT_HOST,
    port: Optional[int] = Option(None, callback=get_port, help=PORT_HELP),
    log_level: Optional[str] = None,
    reload: Optional[bool] = None,
):
    """Starts the web server."""
    kwargs = {
        "host": host,
        "port": port or getenv("PORT"),
        "log_level": log_level,
        "reload": reload,
    }
    kwargs = {key: value for key, value in kwargs.items() if value}
    run("triathlon_live_calendar:app", **kwargs)


@app.command()
def generate(path: Path, verbose: bool = False):
    """Generates the calendar .ics file"""
    logger = Logger(use_typer_echo=True) if verbose else None
    contents = asyncio.run(calendar(logger))
    path.write_text(str(contents))


if __name__ == "__main__":
    app()
