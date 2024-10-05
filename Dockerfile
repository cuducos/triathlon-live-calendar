FROM python:3.11-slim-bookworm AS builder
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
RUN pip install poetry && poetry config virtualenvs.in-project true
COPY pyproject.toml poetry.lock ./
RUN poetry install

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/.venv .venv/
COPY /triathlon_live_calendar ./triathlon_live_calendar
CMD ["/app/.venv/bin/python", "-m", "triathlon_live_calendar", "web"]
