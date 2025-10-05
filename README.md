# Project Template: AI-Ready Web Platform

## Why This Template

This repository is a production-grade starter kit for building modern, AI-assisted products that need to scale from MVP to enterprise. It packages opinionated best practices so humans and code-generation agents can collaborate without re-architecting the stack for every new idea (SEO content site, e-commerce, trading bot control plane, Telegram mini app, fintech dashboard, etc.).

## Highlights

- **Full-stack, batteries-included**: FastAPI + PostgreSQL + Redis backend, Next.js + Tailwind + shadcn/ui frontend, Docker-first infrastructure, and GitHub Actions CI/CD.
- **AI-aware workflows**: Documentation and scripts guide Codex CLI, Claude Code, and other agents through safe plans—covering migrations, tests, linting, type generation, and deployment considerations.
- **Secure user platform**: Unified auth (password, future providers), pre-auth session state, and RBAC/permission scaffolding that extend across API, background tasks, and UI routing.
- **Async & realtime ready**: Redis-backed Arq workers with scheduled/event/continuous jobs, websocket broadcasting for live updates, and patterns for long-running or event-driven integrations.
- **Multi-channel API**: POST-only JSON endpoints modelled after Stripe/Twitter style APIs to serve web, bots, mobile apps, and external partners consistently.
- **Observability baked in**: Loguru structured logs and Sentry instrumentation across backend, workers, and frontend.

## Stack Overview

| Area       | Tools & Frameworks |
|------------|--------------------|
| Backend    | FastAPI, SQLAlchemy 2.x async, Alembic, PostgreSQL, Redis, Arq, Loguru, Sentry |
| Frontend   | Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS, shadcn/ui, Radix UI, Redux Toolkit, TanStack Query, next-themes |
| Testing    | Pytest + pytest-asyncio, Vitest + Testing Library |
| Tooling    | `uv` package manager, Ruff, Prettier, ESLint, openapi-typescript |
| CI/CD      | GitHub Actions, Docker (backend, worker, frontend images), Docker Swarm-ready configs |

## Repository Layout

```
.
├── backend/                # FastAPI app, models, services, tasks, Alembic, tests
├── frontend/               # Next.js app router project with feature-based organization
├── infrastructure/         # NGINX config and deployment artefacts
├── docs/                   # Architecture, AI playbook, operational guides
├── .github/workflows/      # CI (lint/test) and deploy pipelines
├── docker-compose.yml      # Local/dev environment orchestration
├── Makefile                # Common automation tasks
└── .env.example            # Baseline environment variables
```

## Quick Start

1. **Clone & configure**
   ```bash
   cp .env.example .env
   ```

2. **Install dependencies**
   ```bash
   make backend-install
   make frontend-install
   ```

3. **Run the stack locally**
   ```bash
   make docker-up
   # Backend available at http://localhost:8000
   # Frontend available at http://localhost:3000
   ```

4. **Run database migrations**
   ```bash
   cd backend
   uv run alembic upgrade head
   ```

5. **Generate OpenAPI + TypeScript bindings**
   ```bash
   make openapi
   make schema-types
   ```

6. **Validate**
   ```bash
   make backend-test
   make frontend-test
   make lint
   ```

## Development Workflow (Human & AI)

1. Read `docs/architecture.md` and `docs/ai-playbook.md` to understand domain boundaries and agent workflow expectations.
2. Use Codex CLI/Claude Code planning output to list migrations, API changes, tests, and frontend impacts before editing.
3. Implement backend components (models, services, routes) with matching migrations and update schemas/tests.
4. Export OpenAPI + regenerate TypeScript types, then implement frontend feature slices/components.
5. Ensure tests and linters are green; update docs if behaviour changes.

## Key Features Ready to Extend

- **Auth & RBAC**: `backend/app/services/auth.py` and `backend/app/services/access.py` include session bootstrap, token rotation, and role-permission scaffolding.
- **Content Domain**: User-facing posts module demonstrates patterns for create/update/read, pagination, and permission checks.
- **Async Tasks**: `backend/app/tasks/` contains examples for scheduled cleanups, event broadcasts, and long-running polls.
- **Realtime**: `backend/app/api/v1/realtime.py` + `app/utils/realtime.py` provide websocket connection management ready for notifications and progress streams.
- **Frontend Admin Console**: `/app` routes show how to compose dashboard views, fetch data via `useApiClient`, and respect theme/locale in shared components.

## Deployment

- **Docker Compose** for local and dev environments.
- **Dockerfiles** for backend/worker/frontend to publish images (see `.github/workflows/deploy.yml`).
- Integrate with Docker Swarm, Kubernetes, or other orchestrators by extending the provided workflow steps.

## Observability & Ops

- Configure `SENTRY_DSN` / `NEXT_PUBLIC_SENTRY_DSN` to enable Sentry monitoring.
- Logs emit to stdout via Loguru; attach Docker logging drivers or external collectors as needed.
- `docs/operations.md` details routine tasks (migrations, type generation, deployment).

## Contributing

1. Fork and create feature branches.
2. Follow the AI playbook for planning/testing.
3. Run `make lint` and tests before opening a PR.
4. Document migrations, new endpoints, and UI changes in PR summaries.

Ready to build your next AI-assisted product? Start by customising the domain models, hooking up your providers, and letting your coding agents iterate safely within this architecture.
