from datetime import timedelta
from re import compile, findall
from typing import Tuple

from arrow import get  # type: ignore
from httpx import AsyncClient
from ics import Event  # type: ignore
from pyquery import PyQuery  # type: ignore


BASE_URL = "https://www.triathlonlive.tv/upcoming-live-streams"
DEFAULT_DURATION = timedelta(hours=3)
DATETIME_REGEX = compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [+-]*\d{4}")
DATETIME_FORMAT = "YYYY-MM-DD HH:mm:ss Z"


async def event_urls(client: AsyncClient) -> Tuple[str, ...]:
    response = await client.get(BASE_URL)
    dom = PyQuery(response.content)
    urls = (link.attrib.get("href") for link in dom("a.browse-item-link"))
    return tuple(str(url) for url in urls if url)


async def event_from(client: AsyncClient, url: str) -> Event:
    response = await client.get(url)
    dom = PyQuery(response.content)
    title, *_ = dom("h1 strong")
    begin, *_ = findall(DATETIME_REGEX, str(response.content))
    return Event(
        name=title.text,
        begin=get(begin, DATETIME_FORMAT),
        duration=DEFAULT_DURATION,
        url=url,
    )
