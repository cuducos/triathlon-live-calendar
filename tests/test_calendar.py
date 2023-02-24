from asyncio import run
from logging import DEBUG
from unittest.mock import AsyncMock, patch

from ics import Event

from triathlon_live_calendar.calendar import calendar


def test_calendar():
    with (
        patch("triathlon_live_calendar.calendar.event_urls") as event_urls,
        patch("triathlon_live_calendar.calendar.event_from") as events_from,
        patch("triathlon_live_calendar.calendar.AsyncClient") as client,
    ):
        event_urls.return_value = (
            "https://triathlonlive.tv/42",
            "https://triathlonlive.tv/21",
        )
        events_from.side_effect = (Event(name="Fourty Two"), Event(name="Twenty One"))
        client.return_value.__aenter__.return_value = AsyncMock()

        logger = DEBUG
        cal = run(calendar(logger=logger))

        assert events_from.call_count == 2
        events_from.assert_any_call(
            client.return_value.__aenter__.return_value,
            "https://triathlonlive.tv/42",
            logger,
        )
        events_from.assert_any_call(
            client.return_value.__aenter__.return_value,
            "https://triathlonlive.tv/21",
            logger,
        )

    assert len(cal.events) == 2
    assert {"Fourty Two", "Twenty One"} == {e.name for e in cal.events}
