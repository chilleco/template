from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.core.logging import get_logger
from app.core.settings import settings
from app.events.lifecycle import register_lifecycle

logger = get_logger(context="app")


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        docs_url=settings.docs_url,
        openapi_url=settings.openapi_url,
    )

    if settings.cors_allow_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.cors_allow_origins],
            allow_credentials=settings.cors_allow_credentials,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    register_lifecycle(app)
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:  # pragma: no cover
        logger.exception("Unhandled error")
        return JSONResponse(status_code=500, content={"detail": "internal_error"})

    return app


app = create_application()
