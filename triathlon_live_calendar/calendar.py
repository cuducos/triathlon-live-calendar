from asyncio import gather

from httpx import AsyncClient
from ics import Calendar

from triathlon_live_calendar.scraper import event_from, event_urls
from triathlon_live_calendar.logger import Logger


async def calendar(logger: Logger) -> Calendar:
    async with AsyncClient() as client:
        urls = await event_urls(client, logger)
        requests = tuple(event_from(client, url, logger) for url in urls)
        events = await gather(*requests)
    return Calendar(events=set(events))
