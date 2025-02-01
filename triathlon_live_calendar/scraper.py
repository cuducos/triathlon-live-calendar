from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import AsyncGenerator

from httpx import AsyncClient
from ics import Event
from orjson import loads
from pyquery import PyQuery

from triathlon_live_calendar.logger import Logger

URL = "https://triathlonlive.tv/"
USER_AGENT = "triathlon-live-calendar/0.0.2"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
DEFAULT_DURATION = timedelta(hours=3)


class ScraperInitError(Exception): ...


def to_event(data: dict, logger: Logger) -> Event:
    name = data["name"]
    url = f"{URL}video/{data['token']}"
    begin = datetime.strptime(data["start_time"], DATE_FORMAT).replace(
        tzinfo=timezone.utc
    )
    logger.debug((f"Parsed {url}", f"  Title: {name}", f"  Begin: {begin}"))
    return Event(
        name=name,
        begin=begin,
        duration=DEFAULT_DURATION,
        url=url,
        uid=data["token"],
    )


@dataclass
class Scraper:
    API = "https://apiv3.videoflow.io/"
    HEADERS = {"User-Agent": USER_AGENT, "Origin": URL}

    token: str
    page: str

    async def json(self, client, section=None) -> AsyncGenerator[dict, None]:
        url = f"{self.API}ch/{self.token}/pages/{self.page}/sections"
        if section:
            url = f"{url}/{section}/content"
        response = await client.get(url, headers=self.HEADERS)
        for data in response.json().get("data", ()):
            yield data

    async def sections(self, client: AsyncClient) -> AsyncGenerator[str, None]:
        async for section in self.json(client):
            yield section["token"]

    async def events(self, logger: Logger) -> AsyncGenerator[Event, None]:
        async with AsyncClient() as client:
            async for section in self.sections(client):
                async for event in self.json(client, section):
                    if not (data := event.get("input")):
                        continue
                    yield to_event(data, logger)

    @classmethod
    async def init(cls) -> "Scraper":
        async with AsyncClient() as client:
            response = await client.get(
                URL, headers={"User-Agent": USER_AGENT}, follow_redirects=True
            )
            dom = PyQuery(response.text)
            script, *_ = dom('script[type="application/json"]')
            data = loads(script.text)
            channel = data["props"]["pageProps"]["channelData"]
            token = channel["token"]
            page = None
            for nav in channel["header"]["navigation"]:
                if nav.get("name", "").lower() != "calendar":
                    continue
                page = nav["url"]
                break

            if not page:
                raise ScraperInitError(f"Could not find token and URL in {URL}")

            return cls(token, page)
