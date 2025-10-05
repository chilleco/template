# Modern Full-Stack Template

Production-ready, AI-optimized template for scalable web applications.

## Stack

**Backend:**
- Python 3.12+
- FastAPI
- uv (package manager)
- PostgreSQL
- Redis
- SQLAlchemy + Alembic
- loguru

**Frontend:**
- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS
- Radix UI + shadcn/ui
- Redux Toolkit
- React Query

**DevOps:**
- Docker + Docker Compose
- GitHub Actions
- Docker Swarm
- NGINX

## Features

- ✅ Multi-provider authentication (email, phone, username, OAuth)
- ✅ Pre-auth session tokens for anonymous user actions
- ✅ RBAC permissions system
- ✅ Background tasks (scheduled, event-driven, regular)
- ✅ Sentry error tracking
- ✅ WebSocket support
- ✅ POST-only JSON API
- ✅ Mobile-first responsive design
- ✅ Theme support (dark/light/system)
- ✅ i18n (en, ru, es, zh, ar)
- ✅ SEO optimization (SSR for public pages)
- ✅ 100% test coverage

## Quick Start

### Local Development

```bash
# Clone and setup
git clone <repo-url>
cd template3

# Start all services
docker compose up -d

# Backend will be available at http://localhost:8000
# Frontend will be available at http://localhost:3000
# API docs at http://localhost:8000/docs
```

### Manual Setup

**Backend:**
```bash
cd backend
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
.
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Core functionality (config, security, db)
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic
│   │   ├── tasks/       # Background tasks
│   │   ├── integrations/# External API clients
│   │   └── ws/          # WebSocket handlers
│   ├── tests/           # Backend tests
│   └── alembic/         # Database migrations
├── frontend/            # Next.js application
│   ├── src/
│   │   ├── app/         # Next.js app router
│   │   ├── components/  # React components
│   │   ├── lib/         # Utilities
│   │   ├── store/       # Redux store
│   │   └── types/       # TypeScript types
│   └── tests/           # Frontend tests
├── docker/              # Docker configurations
├── .github/             # GitHub Actions workflows
└── nginx/               # NGINX configuration
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

**Backend:**
- `DATABASE_URL`: PostgreSQL connection
- `REDIS_URL`: Redis connection
- `SECRET_KEY`: JWT signing key
- `SENTRY_DSN`: Sentry error tracking
- OAuth credentials

**Frontend:**
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `NEXT_PUBLIC_WS_URL`: WebSocket URL
- `NEXT_PUBLIC_SENTRY_DSN`: Sentry DSN

## AI Code Generation

This template is optimized for AI code generation. See [AI_GUIDELINES.md](AI_GUIDELINES.md) for:
- Code generation workflow
- Project conventions
- Component patterns
- Testing requirements

## Testing

```bash
# Backend tests
cd backend
pytest --cov=app --cov-report=html

# Frontend tests
cd frontend
npm test
npm run test:coverage
```

## Deployment

### Docker Swarm

```bash
docker stack deploy -c docker-stack.yml app
```

### Environment-specific builds

```bash
# Development
docker compose -f docker-compose.yml up

# Production
docker compose -f docker-compose.prod.yml up
```

## Documentation

- [API Documentation](http://localhost:8000/docs) - OpenAPI/Swagger
- [AI Guidelines](AI_GUIDELINES.md) - AI code generation guide
- [Architecture](docs/ARCHITECTURE.md) - System architecture
- [Contributing](docs/CONTRIBUTING.md) - Development guidelines

## License

MIT
