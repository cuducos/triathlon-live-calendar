from asyncio import gather

from httpx import AsyncClient
from ics import Calendar  # type: ignore

from triathlon_live_calendar.scraper import event_from, event_urls


async def calendar() -> Calendar:
    async with AsyncClient() as client:
        urls = await event_urls(client)
        requests = tuple(event_from(client, url) for url in urls)
        events = await gather(*requests)
    return Calendar(events=set(events))
