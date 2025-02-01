from ics import Calendar

from triathlon_live_calendar.logger import Logger
from triathlon_live_calendar.scraper import Scraper


async def calendar(logger: Logger) -> Calendar:
    scraper = await Scraper.init()
    events = set()
    async for event in scraper.events(logger):
        events.add(event)
    return Calendar(events=events)
