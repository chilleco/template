# AI-Native Project Template

A batteries-included template for building modern products with AI copilots. It ships a FastAPI backend, Next.js frontend, Dockerized infrastructure, and workflows tuned for Codex CLI or Claude Code assisted development.

## Quick Start

```bash
make install-backend
make install-frontend
make dev-backend
make dev-frontend
```

Visit `http://localhost:3000` (frontend) and `http://localhost:8000/api/docs` (backend).

Alternatively, run the full stack with Docker:

```bash
docker compose up --build
```

## Repository Layout

- `backend/` – FastAPI service, async task engine, auth, RBAC, integrations.
- `frontend/` – Next.js App Router app with Tailwind, Redux Toolkit, next-intl, shadcn UI primitives.
- `infra/` – Docker Swarm and NGINX configs for staging/production.
- `docs/` – Architecture notes, AI workflow playbook, component overviews.
- `scripts/` – Utility scripts (OpenAPI export, forthcoming codegen helpers).

## Features

- **Universal API**: JSON-only POST-first API supporting web, mobile, and bot clients.
- **Auth & RBAC**: Multi-identifier login, JWT access/refresh tokens, Redis-backed session snapshots, role-based permissions.
- **Background Tasks**: Async registry for periodic, event-driven, and sequential jobs. Redis-backed queue with worker entrypoint.
- **Observability**: Loguru logging, Sentry hooks, structured error propagation.
- **Frontend Excellence**: Mobile-first components, dark/light themes, locale routing, React Query caching, Vitest tests.
- **Infrastructure**: Dockerfiles, Compose, Swarm manifest, GitHub Actions CI (lint + test + build).
- **AI Workflow Guardrails**: Planning prompts, schema generation scripts, documentation for copilots.

## Extending

1. Review docs in `docs/`—especially `ARCHITECTURE.md` and `AI_WORKFLOW.md`.
2. Implement backend changes (models → migrations → services → routes → tests).
3. Export OpenAPI (`python scripts/export_openapi.py openapi`) and sync TypeScript schemas.
4. Build frontend components/hooks, update locales, and cover with tests.
5. Run `make test-backend`, `make test-frontend`, `make lint-backend`, `make lint-frontend` before committing.

## Deployment

- Build images: `docker build -t ghcr.io/your-org/ai-template-backend ./backend` and `...-frontend ./frontend`.
- Push to registry; update tags in `infra/docker-compose.prod.yml`.
- Deploy via Docker Swarm: `docker stack deploy -c infra/docker-compose.prod.yml ai-template`.

## Tooling Notes

- Python dependency management via `uv`. Create a virtualenv with `uv sync`.
- Frontend uses `pnpm`; `corepack enable pnpm` before installing dependencies.
- Code style enforced with Ruff (backend) and ESLint + Prettier (frontend).

## License

MIT – customize and adapt freely.
