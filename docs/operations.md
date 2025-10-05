# Operations Guide

## Local development

1. Copy `.env.example` to `.env` and tweak secrets/URLs.
2. Install dependencies:
   - `make backend-install`
   - `make frontend-install`
3. Start services with Docker: `make docker-up` (FastAPI at `:8000`, Next.js at `:3000`).
4. Run migrations: `cd backend && uv run alembic upgrade head`.

## Testing

- Backend: `make backend-test`
- Frontend: `make frontend-test`
- Lint/format: `make lint` / `make format`

## Generating types

- Export OpenAPI: `make openapi`
- Build TypeScript types: `make schema-types`

## Background workers

Arq worker uses the same image as the API. To run locally:

```bash
uv run arq app.workers.worker.WorkerSettings
```

## Deployment

- Build images: `docker compose build`
- Push to registry (CI handles via GitHub Actions).
- Deploy via Docker Swarm example stack (see `.github/workflows/deploy.yml`).

## Observability

- Configure `SENTRY_DSN` in environment variables to enable tracing.
- Logs stream to stdout via Loguru; ship to your aggregator of choice (e.g., Loki) using Docker logging drivers.

## Secrets & configuration

All configuration flows through environment variables (12-factor). Use `.env` for local dev and secret managers (AWS SM, Doppler, etc.) for production.
