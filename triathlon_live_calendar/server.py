from fastapi import FastAPI, Response

from triathlon_live_calendar.scraper import calendar


app = FastAPI()


@app.get("/")
async def home(response: Response):
    response.headers["Content-type"] = "text/calendar"
    return str(await calendar())
