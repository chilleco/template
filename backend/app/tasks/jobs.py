"""Sample background jobs demonstrating the async task registry."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime

from loguru import logger

from app.tasks.registry import event_handler, periodic_task, sequential_task, task_registry


@periodic_task(name="purge-stale-session-snapshots", interval=60 * 15)
async def purge_session_snapshots() -> None:
    # Placeholder for redis cleanup logic.
    logger.info("[tasks] Purging stale session snapshots at {}", datetime.now(UTC))


@event_handler("user.registered")
async def handle_user_registered(payload: dict) -> None:
    logger.info("[tasks] Dispatching welcome flow for user {}", payload.get("user_id"))


@sequential_task(name="analytics-export")
async def analytics_export(payload: dict) -> None:
    logger.info("[tasks] Processing analytics export {}", payload)
    await asyncio.sleep(0.1)
