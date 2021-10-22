from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from triathlon_live_calendar.cache import Cache
from triathlon_live_calendar.calendar import calendar


DEFAULT_HEADERS = {
    "Content-type": "text/calendar",
    "Content-Disposition": 'attachment; filename="triathlon_live.ics"',
}


app = FastAPI()
cache = Cache()


@app.get("/", response_class=PlainTextResponse)
async def home(response: PlainTextResponse):
    response.headers.update(DEFAULT_HEADERS)

    cached = cache.response
    if cached:
        return cached

    contents = str(await calendar())
    cache.save(contents)
    return contents
