from datetime import timedelta
from hashlib import md5
from re import compile, findall
from time import tzname
from typing import Optional, Tuple

from arrow import get  # type: ignore
from httpx import AsyncClient
from ics import Event  # type: ignore
from pyquery import PyQuery  # type: ignore

from triathlon_live_calendar.logger import Logger


BASE_URL = "https://www.triathlonlive.tv/upcoming-live-streams"
DEFAULT_DURATION = timedelta(hours=3)
DATETIME_REGEX = compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [+-]*\d{4}")
DATETIME_FORMAT = "YYYY-MM-DD HH:mm:ss Z"


async def event_urls(client: AsyncClient) -> Tuple[str, ...]:
    response = await client.get(BASE_URL)
    dom = PyQuery(response.content)
    urls = (link.attrib.get("href") for link in dom("a.browse-item-link"))
    return tuple(str(url) for url in urls if url)


async def event_from(client: AsyncClient, url: str, logger: Optional[Logger]) -> Event:
    response = await client.get(url)
    dom = PyQuery(response.content)
    title, *_ = dom("h1 strong")
    begin, *_ = findall(DATETIME_REGEX, str(response.content))

    begin = get(begin, DATETIME_FORMAT)
    title = title.text.strip()

    if logger:
        tz, *_ = tzname
        local = begin.to(tz).format(DATETIME_FORMAT[:-2])
        logger.debug((f"Parsed {url}", f"  Title: {title}", f"  Begin: {local}"))

    return Event(
        name=title,
        begin=begin,
        duration=DEFAULT_DURATION,
        url=url,
        uid=md5(url.encode("utf-8")).hexdigest(),
    )
