.PHONY: backend-install frontend-install backend-test frontend-test lint format docs openapi docker-up docker-down

backend-install:
	cd backend && uv pip install --system .[dev]

frontend-install:
	cd frontend && npm install

backend-test:
	cd backend && uv run pytest

frontend-test:
	cd frontend && npm run test

lint:
	cd backend && uv run ruff check .
	cd frontend && npm run lint

format:
	cd backend && uv run ruff format .
	cd frontend && npm run lint -- --fix

openapi:
	cd backend && uv run python scripts/generate_ts_schemas.py

schema-types:
	cd frontend && npm run generate:schema

docker-up:
	docker compose up --build

docker-down:
	docker compose down -v
