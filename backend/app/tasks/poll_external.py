from __future__ import annotations

import asyncio

from loguru import logger

from app.tasks.base import ContinuousTask


class PollExternalTask(ContinuousTask):
    name = "poll_external"

    async def run(self) -> None:
        logger.debug("Polling external integration placeholder")
        await asyncio.sleep(5)


task = PollExternalTask()
