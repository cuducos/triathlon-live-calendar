from fastapi import FastAPI, Response

from triathlon_live_calendar.scraper import calendar
from triathlon_live_calendar.cache import Cache


app = FastAPI()
cache = Cache()


@app.get("/")
async def home(response: Response):
    response.headers["Content-type"] = "text/calendar"
    return str(await calendar())
    cached = cache.response
    if cached:
        return cached

    contents = str(await calendar())
    cache.save(contents)
    return contents
