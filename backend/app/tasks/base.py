from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar

from loguru import logger


class TaskContext:
    def __init__(self, **kwargs: Any) -> None:
        self.data = kwargs

    def __getattr__(self, item: str) -> Any:
        return self.data.get(item)


class BaseTask(ABC):
    name: ClassVar[str]
    max_retries: ClassVar[int] = 3

    def __init__(self, context: TaskContext | None = None) -> None:
        self.context = context or TaskContext()

    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        try:
            return await self.run(*args, **kwargs)
        except Exception as exc:  # pragma: no cover - delegated to runner
            logger.exception("Task %s failed", self.name)
            raise exc

    @abstractmethod
    async def run(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class ScheduledTask(BaseTask):
    cron: ClassVar[str]


class EventTask(BaseTask):
    queue: ClassVar[str] = "events"


class ContinuousTask(BaseTask):
    async def run_forever(self, *args: Any, **kwargs: Any) -> None:
        while True:
            await self.run(*args, **kwargs)
