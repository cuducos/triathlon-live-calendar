# Triathlon Live Calendar

Calendar file generator for [TriathlonLive](https://www.triathlonlive.tv/) upcoming events.

## Requirements

* [Python](https://python.org) 3.12 or newer
* [`uv`](https://docs.astral.sh/uv/)

## Running

Starting the web server in development mode:

```console
$ uv run python -m triathlon_live_calendar web --reload --log-level=debug
```

Generating the `.ics` file locally:

```console
$ uv run python -m triathlon_live_calendar generate tri-calendar.ics
```

Try `python -m triathlon_live_calendar --help` for more details ; )

## Contributing

Please, write and run tests:

```console
$ uv run pytest
```
