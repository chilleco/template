"""FastAPI application entrypoint with lifecycle management and router wiring."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.sentry import configure_sentry
from app.tasks.scheduler import schedule_background_jobs


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    configure_sentry()
    await settings.setup()
    schedule_background_jobs()

    yield

    await settings.shutdown()


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.project_name,
        version=settings.version,
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_methods=settings.allow_methods,
        allow_headers=settings.allow_headers,
        allow_credentials=True,
    )

    app.include_router(api_router)
    return app


app = create_application()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.reload,
        loop="asyncio",
    )
