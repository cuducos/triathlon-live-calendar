# Triathlon Live Calendar

Calendar file generator for triathlonlive.tv upcoming events.

## Install

Requires [Python](https://python.org) 3.9.7 and [Poetry](https://python-poetry.org).

```console
$ poetry install
```

## Running

```console
$ poetry run uvicorn triathlon_live_calendar:app --reload --log-level=debug
```

## Contributing

```console
$ poetry run black .
$ poetry run mypy .
$ poetry run flake8 **/*.py --ignore=E501
```
