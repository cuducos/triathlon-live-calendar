from datetime import timedelta
from hashlib import md5
from re import compile, findall
from time import tzname
from typing import Tuple

from arrow import get
from httpx import AsyncClient
from ics import Event
from pyquery import PyQuery

from triathlon_live_calendar.logger import Logger


BASE_URL = "https://www.triathlonlive.tv/upcoming-live-streams"
DEFAULT_DURATION = timedelta(hours=3)
DATETIME_REGEX = compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [+-]*\d{4}")
DATETIME_FORMAT = "YYYY-MM-DD HH:mm:ss Z"


async def event_urls(client: AsyncClient, logger: Logger) -> Tuple[str, ...]:
    urls, page = set(), 0
    while True:
        page += 1
        url = f"{BASE_URL}?page={page}"

        logger.debug(f"Requesting: {url}")
        response = await client.get(url)
        if response.status_code < 200 and response.status_code >= 300:
            break

        dom = PyQuery(response.content)
        links = dom("a.browse-item-link")
        if not links:
            break

        for link in links:
            event_url = link.attrib.get("href")
            logger.debug(f"Found: {event_url}")
            urls.add(event_url)

    return tuple(str(url) for url in urls if url)


async def event_from(client: AsyncClient, url: str, logger: Logger) -> Event:
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
