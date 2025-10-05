# syntax=docker/dockerfile:1.6

FROM ghcr.io/astral-sh/uv:python3.12-bookworm as deps
WORKDIR /app
COPY pyproject.toml ./
RUN uv sync --frozen --no-install-project
COPY . .
RUN uv sync --frozen

FROM python:3.12-slim as runner
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app
COPY --from=deps /app/.venv /.venv
COPY app ./app
COPY alembic.ini ./alembic.ini
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
