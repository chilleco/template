"""Standalone worker entrypoint for running the async task registry."""

from __future__ import annotations

import asyncio

from loguru import logger

from app.core.config import settings
from app.core.logging import configure_logging
from app.tasks.scheduler import schedule_background_jobs
from app.tasks.registry import task_registry


async def main() -> None:
    configure_logging()
    await settings.setup()
    schedule_background_jobs()
    logger.info("Worker started. Awaiting tasks…")
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:  # noqa: PERF203
        logger.info("Worker shutting down")
    finally:
        await settings.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
