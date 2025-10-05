from __future__ import annotations

from fastapi import FastAPI

from app.core.logging import configure_logging
from app.core.telemetry import configure_sentry


def register_lifecycle(app: FastAPI) -> None:
    configure_logging()
    configure_sentry()

    @app.on_event("startup")
    async def _startup() -> None:  # pragma: no cover
        pass

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # pragma: no cover
        pass
