# Triathlon Live Calendar

Calendar file generator for triathlonlive.tv upcoming events.

## Install

Requires [Python](https://python.org) 3.11.2 and [Poetry](https://python-poetry.org).

```console
$ poetry install
```

## Running

Starting the web server in development mode:

```console
$ poetry run python -m triathlon_live_calendar web --reload --log-level=debug
```

Generating the `.ics` file locally:

```console
$ poetry run python -m triathlon_live_calendar generate tri-calendar.ics
```

Try `python -m triathlon_live_calendar --help` for more details ; )

## Contributing

Please, write and run tests:

```console
$ poetry run pytest
```
