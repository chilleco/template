# Architecture Overview

## Monorepo layout

```
.
├── backend/              # FastAPI application, async task workers, Alembic migrations
├── frontend/             # Next.js 14 app router project with Tailwind/shadcn/Redux
├── infrastructure/       # Container orchestration assets (NGINX, Docker)
├── docs/                 # Architecture and AI collaboration guides
├── docker-compose.yml    # Local/dev orchestration
├── Makefile              # Common automation entry points
└── .github/workflows/    # CI/CD pipelines
```

## Backend services

- **FastAPI** with modular routers (`app/api`) and domain-driven services (`app/services`).
- **SQLAlchemy 2.0** async stack targeting PostgreSQL/asyncpg; migrations via Alembic.
- **Authentication** supports password, future OAuth/OTP providers, pre-auth session tokens, and RBAC policies.
- **Redis + Arq** handles async workloads with scheduled, event-driven, and continuous task patterns.
- **Loguru + Sentry** power structured logging and error observability across HTTP, workers, and websockets.
- **Client abstraction layer** (`app/clients`) standardises integration with external APIs (payments, messaging, etc.).
- **Universal POST-only API** emphasises typed request/response contracts for multi-channel clients (web, bots, mobile).

## Frontend platform

- Next.js App Router with React Server Components, co-located feature modules, and SEO-friendly marketing surfaces.
- Tailwind CSS + shadcn/ui + Radix provide accessible UI primitives with a themeable design system.
- Redux Toolkit stores security/identity state; TanStack Query orchestrates server communication.
- Localisation (Next Intl), theming (next-themes), and responsive-first component design ensure multi-market readiness.
- Type-safe bindings to backend generated through `openapi-typescript` + backend export script.

## Async task orchestration

Three task archetypes defined in `app/tasks`:

- `ScheduledTask`: cron-style jobs (e.g., session cleanup) executed via Arq cron definitions.
- `EventTask`: ad-hoc workloads triggered by API events, queueable for scale-out processing.
- `ContinuousTask`: long-running loops for polling third-party systems or pipelines.

## Realtime messaging

`app/utils/realtime.py` maintains websocket sessions and broadcast helpers, allowing background tasks to push updates (e.g., job completions) to connected clients.

## Observability & resilience

- Loguru structured logging with contextual bindings.
- Sentry instrumentation across FastAPI, SQLAlchemy, Redis, and front-end with release environments.
- Centralised error handler ensures redaction while preserving traceability.

## Deployment targets

- Docker Compose for local/dev parity.
- Dockerfiles for backend/worker/frontend to support Swarm/Kubernetes rollouts behind NGINX ingress.
- GitHub Actions workflow templates for CI (lint/test) and CD (image builds, swarm deploy placeholders).
