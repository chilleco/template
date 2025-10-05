.PHONY: help install-backend install-frontend dev-backend dev-frontend test-backend test-frontend lint-backend lint-frontend format

help:
	@echo "Targets:"
	@echo "  install-backend  Install backend dependencies via uv"
	@echo "  install-frontend Install frontend dependencies via pnpm"
	@echo "  dev-backend      Run FastAPI in reload mode"
	@echo "  dev-frontend     Run Next.js app"
	@echo "  test-backend     Run backend tests"
	@echo "  test-frontend    Run frontend tests"
	@echo "  lint-backend     Run ruff lint"
	@echo "  lint-frontend    Run next lint"

install-backend:
	cd backend && uv sync

install-frontend:
	cd frontend && pnpm install

dev-backend:
	cd backend && uv run uvicorn app.main:app --reload

dev-frontend:
	cd frontend && pnpm dev

test-backend:
	cd backend && uv run pytest

test-frontend:
	cd frontend && pnpm test

lint-backend:
	cd backend && uv run ruff check app tests

lint-frontend:
	cd frontend && pnpm lint

format:
	cd frontend && pnpm format
