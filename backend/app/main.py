"""FastAPI application entry point."""
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.core.config import settings
from app.core.database import close_db, init_db
from app.core.redis import redis_client
from app.core.logging import setup_logging, setup_sentry
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    http_exception_handler,
    general_exception_handler,
)
from fastapi import HTTPException


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan events.

    Handles startup and shutdown:
    - Initialize logging and Sentry
    - Connect to Redis
    - Initialize database (dev only)
    - Cleanup on shutdown
    """
    # Startup
    setup_logging()
    setup_sentry()

    # Connect to Redis
    await redis_client.connect()

    # Initialize database (only in local/dev)
    if settings.ENVIRONMENT in ["local", "development"]:
        await init_db()

    yield

    # Shutdown
    await redis_client.disconnect()
    await close_db()


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Modern full-stack template with FastAPI and Next.js",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Exception Handlers
app.add_exception_handler(AppException, app_exception_handler)  # type: ignore
app.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore
app.add_exception_handler(Exception, general_exception_handler)  # type: ignore

# Register API routes
# from app.api import auth, users, posts

# app.include_router(auth.router, prefix=f"{settings.API_PREFIX}/auth", tags=["auth"])
# app.include_router(users.router, prefix=f"{settings.API_PREFIX}/users", tags=["users"])
# app.include_router(posts.router, prefix=f"{settings.API_PREFIX}/posts", tags=["posts"])


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
