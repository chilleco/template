.PHONY: help setup start stop restart logs clean test lint format migrate

# Default target
help:
	@echo "Available commands:"
	@echo "  make setup      - Initial setup (create .env files and start services)"
	@echo "  make start      - Start all services"
	@echo "  make stop       - Stop all services"
	@echo "  make restart    - Restart all services"
	@echo "  make logs       - View logs (Ctrl+C to exit)"
	@echo "  make clean      - Stop and remove all containers and volumes"
	@echo "  make test       - Run all tests"
	@echo "  make lint       - Run linters"
	@echo "  make format     - Format code"
	@echo "  make migrate    - Run database migrations"

# Initial setup
setup:
	@echo "Setting up project..."
	@./setup.sh

# Start services
start:
	@echo "Starting services..."
	@docker compose up -d
	@echo "Services started!"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend:  http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

# Stop services
stop:
	@echo "Stopping services..."
	@docker compose down

# Restart services
restart:
	@echo "Restarting services..."
	@docker compose restart

# View logs
logs:
	@docker compose logs -f

# Clean up
clean:
	@echo "⚠️  This will remove all containers and volumes!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker compose down -v; \
		echo "Cleanup complete!"; \
	fi

# Run tests
test:
	@echo "Running backend tests..."
	@docker compose exec backend pytest
	@echo ""
	@echo "Running frontend tests..."
	@docker compose exec frontend npm test

# Run linters
lint:
	@echo "Linting backend..."
	@docker compose exec backend ruff check .
	@docker compose exec backend mypy .
	@echo ""
	@echo "Linting frontend..."
	@docker compose exec frontend npm run lint

# Format code
format:
	@echo "Formatting backend code..."
	@docker compose exec backend black .
	@echo ""
	@echo "Formatting frontend code..."
	@docker compose exec frontend npm run lint -- --fix

# Run migrations
migrate:
	@echo "Creating migration..."
	@read -p "Migration name: " name; \
	docker compose exec backend alembic revision --autogenerate -m "$$name"
	@echo ""
	@echo "Applying migrations..."
	@docker compose exec backend alembic upgrade head

# Backend specific commands
backend-shell:
	@docker compose exec backend bash

backend-test:
	@docker compose exec backend pytest

backend-coverage:
	@docker compose exec backend pytest --cov=app --cov-report=html
	@echo "Coverage report: backend/htmlcov/index.html"

# Frontend specific commands
frontend-shell:
	@docker compose exec frontend sh

frontend-test:
	@docker compose exec frontend npm test

frontend-build:
	@docker compose exec frontend npm run build

# Database commands
db-shell:
	@docker compose exec postgres psql -U template_user -d template_db

db-reset:
	@echo "⚠️  This will reset the database!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker compose down postgres; \
		docker volume rm template3_postgres_data; \
		docker compose up -d postgres; \
		sleep 5; \
		docker compose exec backend alembic upgrade head; \
		echo "Database reset complete!"; \
	fi

# Redis commands
redis-shell:
	@docker compose exec redis redis-cli -a template_redis_pass

redis-flush:
	@echo "⚠️  This will flush all Redis data!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker compose exec redis redis-cli -a template_redis_pass FLUSHALL; \
		echo "Redis flushed!"; \
	fi
