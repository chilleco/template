"""Async task registry supporting periodic, sequential, and event-driven jobs."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

from app.clients.redis import redis_client
from app.core.config import Settings

PeriodicCallable = Callable[[], Awaitable[None]]
EventCallable = Callable[[dict[str, Any]], Awaitable[None]]
SequentialCallable = Callable[[dict[str, Any]], Awaitable[None]]


@dataclass
class PeriodicTask:
    name: str
    interval: float
    func: PeriodicCallable
    immediate: bool = False


@dataclass
class SequentialTask:
    name: str
    func: SequentialCallable
    _queue: asyncio.Queue[dict[str, Any]] = field(default_factory=asyncio.Queue)


class AsyncTaskRegistry:
    def __init__(self) -> None:
        self.periodic_tasks: list[PeriodicTask] = []
        self.event_handlers: dict[str, list[EventCallable]] = {}
        self.sequential_tasks: dict[str, SequentialTask] = {}
        self._running_tasks: list[asyncio.Task[None]] = []
        self._redis = None
        self._shutdown = asyncio.Event()

    async def setup(self, settings: Settings) -> None:
        self._shutdown.clear()
        self._redis = await redis_client.connect()

    async def shutdown(self) -> None:
        self._shutdown.set()
        for task in self._running_tasks:
            task.cancel()
        self._running_tasks.clear()
        await redis_client.close()

    def register_periodic(self, name: str, interval: float, func: PeriodicCallable, immediate: bool = False) -> None:
        self.periodic_tasks.append(PeriodicTask(name=name, interval=interval, func=func, immediate=immediate))

    def register_event_handler(self, event: str, func: EventCallable) -> None:
        handlers = self.event_handlers.setdefault(event, [])
        handlers.append(func)

    def register_sequential(self, name: str, func: SequentialCallable) -> None:
        self.sequential_tasks[name] = SequentialTask(name=name, func=func)

    def start(self) -> None:
        if self._running_tasks:
            return
        loop = asyncio.get_running_loop()
        for periodic in self.periodic_tasks:
            task = loop.create_task(self._run_periodic(periodic))
            self._running_tasks.append(task)
        for sequential in self.sequential_tasks.values():
            task = loop.create_task(self._run_sequential(sequential))
            self._running_tasks.append(task)

    async def emit(self, event: str, payload: dict[str, Any]) -> None:
        handlers = self.event_handlers.get(event, [])
        await asyncio.gather(*(handler(payload) for handler in handlers))

    async def enqueue(self, queue_name: str, payload: dict[str, Any]) -> None:
        task = self.sequential_tasks.get(queue_name)
        if not task:
            raise ValueError(f"Sequential task '{queue_name}' is not registered")
        await task._queue.put(payload)

    async def _run_periodic(self, task: PeriodicTask) -> None:
        if task.immediate:
            await task.func()
        while not self._shutdown.is_set():
            await asyncio.sleep(task.interval)
            if self._shutdown.is_set():
                break
            await task.func()

    async def _run_sequential(self, task: SequentialTask) -> None:
        while not self._shutdown.is_set():
            payload = await task._queue.get()
            try:
                await task.func(payload)
            finally:
                task._queue.task_done()


task_registry = AsyncTaskRegistry()


def periodic_task(name: str, interval: float, immediate: bool = False):
    def decorator(func: PeriodicCallable) -> PeriodicCallable:
        task_registry.register_periodic(name, interval, func, immediate=immediate)
        return func

    return decorator


def event_handler(event: str):
    def decorator(func: EventCallable) -> EventCallable:
        task_registry.register_event_handler(event, func)
        return func

    return decorator


def sequential_task(name: str):
    def decorator(func: SequentialCallable) -> SequentialCallable:
        task_registry.register_sequential(name, func)
        return func

    return decorator


__all__ = [
    "task_registry",
    "periodic_task",
    "event_handler",
    "sequential_task",
]
