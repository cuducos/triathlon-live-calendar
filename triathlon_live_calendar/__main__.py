import asyncio
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING
from os import getenv
from pathlib import Path
from typing import Optional

from typer import Option, Typer, echo
from uvicorn import run

from triathlon_live_calendar.calendar import calendar
from triathlon_live_calendar.logger import Logger

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000
DEFAULT_LOG_LEVEL = "info"
PORT_HELP = f"[default: {DEFAULT_PORT} or PORT from environment variable]"
LEVELS = {
    "critical": CRITICAL,
    "error": ERROR,
    "warning": WARNING,
    "info": INFO,
    "debug": DEBUG,
}

app = Typer()


def get_port(value: Optional[str]) -> int:
    if value:
        return int(value)

    try:
        return int(getenv("PORT", ""))
    except ValueError:
        return DEFAULT_PORT


def get_log_level(value: str) -> str:
    if value not in LEVELS.keys():
        echo(f"Invalid log level: {value}. Options are: {', '.join(LEVELS.keys())}")
        return DEFAULT_LOG_LEVEL

    return value


@app.command()
def web(
    host: str = DEFAULT_HOST,
    port: Optional[int] = Option(None, callback=get_port, help=PORT_HELP),
    log_level: Optional[str] = Option(None, callback=get_log_level),
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
    run("triathlon_live_calendar:app", **kwargs)  # type: ignore


@app.command()
def generate(
    path: Path,
    log_level: str = Option(DEFAULT_LOG_LEVEL, callback=get_log_level),
):
    """Generates the calendar .ics file"""
    logger = Logger(LEVELS[log_level])
    contents = asyncio.run(calendar(logger))
    path.write_text(contents.serialize())


if __name__ == "__main__":
    app()
