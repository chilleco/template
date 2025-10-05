# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This is a full-stack application with a clean separation between backend and frontend:

**Backend (FastAPI + SQLAlchemy)**
- FastAPI web framework with async/await support
- SQLAlchemy 2.0 with asyncpg for PostgreSQL 
- Repository pattern for data access (`repositories/`)
- Service layer for business logic (`services/`)
- API versioning under `api/v1/`
- Celery for background tasks with Redis broker
- Pydantic schemas for request/response validation
- Poetry/pyproject.toml for dependency management

**Frontend (Next.js + TypeScript)**
- Next.js 13 with TypeScript
- Tailwind CSS for styling with shadcn/ui components
- Feature-Sliced Design architecture (`entities/`, `features/`, `shared/`)
- Generated TypeScript client from OpenAPI schema
- React Hook Form with Zod validation

**Infrastructure**
- Docker Compose for orchestration
- Multiple environment configs (local, dev, prod)
- Traefik for reverse proxy and load balancing
- Terraform for cloud infrastructure

## Common Development Commands

### Backend Development
```bash
# Install dependencies (in backend/)
poetry install --with dev

# Run linting and type checking
poetry run ruff check app/
poetry run ruff format app/
poetry run mypy app/

# Run tests
poetry run pytest
poetry run pytest tests/unit/
poetry run pytest tests/integration/
poetry run pytest tests/e2e/

# Generate TypeScript client
poetry run python -m scripts.generate_ts_client --url http://localhost:8000/openapi.json
```

### Frontend Development
```bash
# Install dependencies (in frontend/)
npm install

# Development server
npm run dev

# Build and linting
npm run build
npm run lint
```

### Docker Operations
```bash
# Local development environment
make up-local
make down-local

# Development environment  
make up-dev
make down-dev

# Production environment
make up
make down

# Run tests in containers
make test

# View logs
make logs        # production
make logs-dev    # development

# Check container status
make status

# Clean environment
make clean
```

## Key Patterns

**Backend Patterns:**
- Use dependency injection via FastAPI's `Depends()`
- Repository pattern for database operations
- Service layer encapsulates business logic
- Async/await throughout for I/O operations
- Pydantic models for API contracts
- Background tasks via Celery workers

**Frontend Patterns:**
- Feature-Sliced Design for code organization
- Generated API client from OpenAPI spec  
- Shared UI components in `shared/ui/`
- Entity-specific components in `entities/`
- Feature-specific logic in `features/`

**Environment Configuration:**
- `.env` file for environment variables
- Different Docker Compose files for different environments
- Environment-specific settings in `app/core/config.py`

## Testing Strategy

- Unit tests for individual functions/classes
- Integration tests for database operations and API endpoints
- End-to-end tests for complete user workflows
- Use `pytest` with async support for backend tests
- Use factory pattern for test data generation

## Database Operations

- SQLAlchemy 2.0 async patterns
- Alembic for database migrations
- Repository pattern abstracts database access
- Use async context managers for database sessions