#!/bin/bash

# Setup script for the template

set -e

echo "🚀 Setting up Modern Full-Stack Template..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Backend setup
echo "📦 Setting up backend..."
cd backend

if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env with your settings"
else
    echo "✅ backend/.env already exists"
fi

cd ..

# Frontend setup
echo "📦 Setting up frontend..."
cd frontend

if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit frontend/.env with your settings"
else
    echo "✅ frontend/.env already exists"
fi

cd ..

# Start Docker services
echo ""
echo "🐳 Starting Docker services..."
docker compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 10

# Run database migrations
echo "🗄️  Running database migrations..."
docker compose exec backend alembic upgrade head

echo ""
echo "✅ Setup complete!"
echo ""
echo "📍 Services are running at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📝 Next steps:"
echo "   1. Edit backend/.env with your settings"
echo "   2. Edit frontend/.env with your settings"
echo "   3. Restart services: docker compose restart"
echo ""
echo "🛠️  Useful commands:"
echo "   View logs:     docker compose logs -f"
echo "   Stop services: docker compose down"
echo "   Restart:       docker compose restart"
echo ""
