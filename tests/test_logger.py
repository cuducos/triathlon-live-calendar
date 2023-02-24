from unittest.mock import patch

import pytest

from triathlon_live_calendar.logger import Logger, multiline


@pytest.mark.parametrize(
    "value,expected",
    (
        ("42", "42"),
        (("4", "2"), "4\n2"),
    ),
)
def test_multiliner_decorator(value, expected):
    @multiline
    def pipe(_, value):
        return value

    assert pipe(None, value) == expected


def test_logger_critical():
    with patch("triathlon_live_calendar.logger.getLogger"):
        log = Logger()
        log.critical("here comes a log")
        log.logger.return_value.critical.asser_called_once_with("here comes a log")


def test_logger_debug():
    with patch("triathlon_live_calendar.logger.getLogger"):
        log = Logger()
        log.debug("here comes a log")
        log.logger.return_value.debug.asser_called_once_with("here comes a log")


def test_logger_error():
    with patch("triathlon_live_calendar.logger.getLogger"):
        log = Logger()
        log.error("here comes a log")
        log.logger.return_value.error.asser_called_once_with("here comes a log")


def test_logger_info():
    with patch("triathlon_live_calendar.logger.getLogger"):
        log = Logger()
        log.info("here comes a log")
        log.logger.return_value.info.asser_called_once_with("here comes a log")


def test_logger_warning():
    with patch("triathlon_live_calendar.logger.getLogger"):
        log = Logger()
        log.warning("here comes a log")
        log.logger.return_value.warning.asser_called_once_with("here comes a log")
