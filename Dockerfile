FROM python:3.11-slim
WORKDIR /app
RUN pip install poetry && useradd -m keller
USER keller
COPY pyproject.toml .
COPY poetry.lock .
COPY triathlon_live_calendar/ .
RUN poetry install
CMD ["poetry", "run", "python", "-m", "triathlon_live_calendar", "web"]
