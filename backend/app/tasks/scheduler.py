"""Task scheduler integration with FastAPI lifespan."""

from __future__ import annotations

from loguru import logger

from app.tasks import jobs  # noqa: F401 ensure task registration side effects
from app.tasks.registry import task_registry


def schedule_background_jobs() -> None:
    logger.debug("Starting background task registry")
    task_registry.start()
