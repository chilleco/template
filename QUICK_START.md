# Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites

- **Docker** and **Docker Compose** installed
- **Git** (optional, for version control)
- **Code editor** (VS Code recommended)

## 1. Automated Setup (Recommended)

```bash
# Run the setup script
./setup.sh

# The script will:
# - Create .env files from examples
# - Start all Docker services
# - Run database migrations
```

## 2. Manual Setup (Alternative)

### Backend Setup

```bash
# Navigate to backend
cd backend

# Copy environment file
cp .env.example .env

# Edit .env with your settings (optional for local dev)
# nano .env
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Copy environment file
cp .env.example .env

# Edit .env with your settings (optional for local dev)
# nano .env
```

### Start Services

```bash
# From project root
docker compose up -d

# View logs
docker compose logs -f
```

### Run Migrations

```bash
# Create initial migration
docker compose exec backend alembic revision --autogenerate -m "Initial migration"

# Apply migration
docker compose exec backend alembic upgrade head
```

## 3. Verify Installation

### Check Services

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Test API

```bash
# Health check
curl http://localhost:8000/health

# Should return: {"status":"healthy"}
```

## 4. Development Workflow

### Backend Development

```bash
# Watch logs
docker compose logs -f backend

# Enter backend container
docker compose exec backend bash

# Run tests
docker compose exec backend pytest

# Create new migration
docker compose exec backend alembic revision --autogenerate -m "Add new field"

# Apply migration
docker compose exec backend alembic upgrade head
```

### Frontend Development

```bash
# Watch logs
docker compose logs -f frontend

# Enter frontend container
docker compose exec frontend sh

# Install new package
docker compose exec frontend npm install package-name

# Run tests
docker compose exec frontend npm test
```

### Database Access

```bash
# Connect to PostgreSQL
docker compose exec postgres psql -U template_user -d template_db

# Common commands:
# \dt          - List tables
# \d users     - Describe users table
# \q           - Quit
```

### Redis Access

```bash
# Connect to Redis
docker compose exec redis redis-cli -a template_redis_pass

# Common commands:
# KEYS *       - List all keys
# GET key      - Get value
# quit         - Exit
```

## 5. Next Steps

### Add Your First Feature

Follow the AI code generation workflow from `AI_GUIDELINES.md`:

1. **Plan** - Define requirements
2. **Models** - Create database models
3. **Tests** - Write test cases
4. **Backend** - Implement API routes
5. **Frontend** - Build UI components

### Example: Add a "Comments" Feature

```bash
# 1. Create model
# Edit: backend/app/models/comment.py

# 2. Create migration
docker compose exec backend alembic revision --autogenerate -m "Add comments"
docker compose exec backend alembic upgrade head

# 3. Create schemas
# Edit: backend/app/schemas/comment.py

# 4. Create routes
# Edit: backend/app/api/comments.py

# 5. Add tests
# Edit: backend/tests/api/test_comments.py

# 6. Run tests
docker compose exec backend pytest

# 7. Update frontend types
# Edit: frontend/src/types/api/comment.ts

# 8. Create components
# Edit: frontend/src/components/comments/
```

## 6. Common Commands

### Docker

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# Restart services
docker compose restart

# View logs
docker compose logs -f [service]

# Rebuild after code changes
docker compose up -d --build

# Remove volumes (⚠️ deletes data)
docker compose down -v
```

### Backend

```bash
# Format code
docker compose exec backend black .

# Lint
docker compose exec backend ruff check .

# Type check
docker compose exec backend mypy .

# Run specific test
docker compose exec backend pytest tests/api/test_users.py

# Coverage report
docker compose exec backend pytest --cov=app --cov-report=html
```

### Frontend

```bash
# Lint
docker compose exec frontend npm run lint

# Type check
docker compose exec frontend npm run type-check

# Build
docker compose exec frontend npm run build

# Run tests
docker compose exec frontend npm test
```

## 7. Troubleshooting

### Port Already in Use

```bash
# Check what's using port 3000
lsof -i :3000

# Kill the process
kill -9 <PID>

# Or change port in docker-compose.yml
```

### Database Connection Error

```bash
# Check if PostgreSQL is running
docker compose ps postgres

# Restart PostgreSQL
docker compose restart postgres

# Check logs
docker compose logs postgres
```

### Frontend Not Loading

```bash
# Check if frontend is running
docker compose ps frontend

# Restart frontend
docker compose restart frontend

# Check logs
docker compose logs frontend

# Rebuild frontend
docker compose up -d --build frontend
```

### Migration Errors

```bash
# Drop all tables (⚠️ deletes data)
docker compose exec backend python -c "from app.core.database import engine, Base; import asyncio; asyncio.run(Base.metadata.drop_all(bind=engine))"

# Recreate tables
docker compose exec backend alembic upgrade head
```

## 8. Production Deployment

See `IMPLEMENTATION.md` for full deployment guide.

Quick production checklist:

- [ ] Change `SECRET_KEY` in backend/.env
- [ ] Set `DEBUG=false` in backend/.env
- [ ] Configure production database
- [ ] Set up Redis with password
- [ ] Configure Sentry DSN
- [ ] Set up SSL certificates
- [ ] Configure NGINX
- [ ] Set up CI/CD pipeline
- [ ] Configure backups
- [ ] Set up monitoring

## Resources

- **Full Documentation**: See `README.md`
- **AI Guidelines**: See `AI_GUIDELINES.md`
- **Implementation Details**: See `IMPLEMENTATION.md`
- **API Docs**: http://localhost:8000/docs (when running)

## Getting Help

- Check existing documentation
- Review code comments
- Examine test files for examples
- Use the AI guidelines for feature development

---

**Ready to build? Start with the AI_GUIDELINES.md workflow!**
