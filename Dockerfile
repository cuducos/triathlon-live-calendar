FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --no-install-project --frozen
COPY /triathlon_live_calendar ./triathlon_live_calendar
CMD ["uv", "run", "python", "-m", "triathlon_live_calendar", "web"]
