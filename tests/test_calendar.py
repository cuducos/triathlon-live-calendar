from logging import DEBUG
from unittest.mock import MagicMock, patch

from ics import Event
from pytest import mark

from triathlon_live_calendar.calendar import calendar
from triathlon_live_calendar.scraper import Scraper


async def mocked_events():
    for event in (Event(name="Forty Two"), Event(name="Twenty One")):
        yield event


@mark.asyncio
async def test_calendar():
    scraper = MagicMock()
    scraper.events.return_value = mocked_events()
    with patch.object(Scraper, "init", return_value=scraper):
        cal = await calendar(logger=DEBUG)
        scraper.events.assert_called_once()
        assert len(cal.events) == 2
        assert {"Forty Two", "Twenty One"} == {e.name for e in cal.events}
