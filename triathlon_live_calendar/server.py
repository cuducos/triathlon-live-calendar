from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from triathlon_live_calendar.cache import Cache
from triathlon_live_calendar.calendar import calendar
from triathlon_live_calendar.logger import Logger


DEFAULT_HEADERS = {
    "Content-type": "text/calendar",
    "Content-Disposition": 'attachment; filename="triathlon_live.ics"',
}


app = FastAPI()
cache = Cache()
logger = Logger()


@app.get("/", response_class=PlainTextResponse)
async def home(response: PlainTextResponse):
    response.headers.update(DEFAULT_HEADERS)

    cached = cache.response
    if cached:
        return cached

    contents = str(await calendar(logger))
    cache.save(contents)
    return contents
