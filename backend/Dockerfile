FROM ghcr.io/astral-sh/uv:python3.11-bookworm

WORKDIR /app
COPY pyproject.toml ./
RUN uv pip install --system .
COPY app ./app
COPY alembic.ini ./alembic.ini
COPY alembic ./alembic
COPY scripts ./scripts

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uv", "run", "fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
