# AI Collaboration Playbook

This repository is optimised for code-generation agents (Codex CLI, Claude Code, etc.). The recommended workflow keeps humans in control while delegating repeatable edits to AI.

## 1. Understand the scope

1. Inspect relevant domain docs (architecture, feature ADRs, API contracts).
2. Identify affected modules (backend service, frontend feature, infra).
3. List compliance hooks (e.g., permissions, locales, telemetry) that must be respected.

## 2. Plan before coding

Agents must produce an execution plan capturing:

- Required models/migrations.
- API changes + schema exports.
- Background tasks or workflows touched.
- Frontend UI/UX impacts (access rules, responsive states, theming, locales).
- Test strategy for backend (100% coverage in touched modules) and frontend (unit + interaction tests).

## 3. Implement backend safely

1. Model changes → create Alembic migration (`uv run alembic revision --autogenerate -m "..."`).
2. Update SQLAlchemy models and Pydantic schemas together.
3. Extend services/routers following POST-only conventions.
4. Refresh OpenAPI spec (`make openapi`) and regenerate TS types (`make schema-types`).
5. Add pytest modules + fixtures that cover happy paths, edge cases, and auth/permission failures.

## 4. Implement background/async work

- Choose appropriate task archetype (`ScheduledTask`, `EventTask`, `ContinuousTask`).
- Ensure idempotency + retries; log contextual info via Loguru.
- Emit websocket broadcasts or Sentry breadcrumbs when useful.

## 5. Frontend delivery

1. Design components under `src/features/<domain>` with co-located hooks/tests.
2. Guard routes/UI using RBAC helpers; respect locales (`next-intl`) and theme tokens.
3. Use generated TS types for API interactions; wrap fetches via `useApiClient`.
4. Validate UI with Vitest/Testing Library.

## 6. Verification & release prep

- `make backend-test` / `make frontend-test` / `make lint` must pass.
- Ensure Docker builds succeed locally (`make docker-up`).
- Update docs/ADR if behaviour or integrations change.
- Provide migration/test execution notes in PR summaries.

Following this disciplined pipeline keeps AI contributions reliable, auditable, and production-safe.
