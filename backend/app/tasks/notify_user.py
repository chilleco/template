from __future__ import annotations

from loguru import logger

from app.tasks.base import EventTask
from app.utils.realtime import connection_manager


class NotifyUserTask(EventTask):
    name = "notify_user"

    async def run(self, payload: dict) -> None:
        logger.info("Notifying user event=%s", payload)
        await connection_manager.broadcast("user_notification", payload)


task = NotifyUserTask()
