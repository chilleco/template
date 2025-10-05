"""Developer tooling CLI leveraging Typer for automation."""

from __future__ import annotations

import asyncio
from typing import Any

import typer

from app.core.config import settings
from app.tasks.registry import task_registry

app = typer.Typer(help="Backend developer utilities")


@app.command()
def emit(event: str, payload: str = "{}") -> None:
    """Emit an event payload to asynchronous handlers."""

    async def _emit() -> None:
        await settings.setup()
        try:
            await task_registry.emit(event, eval(payload))  # noqa: S307 - trusted cli usage
        finally:
            await settings.shutdown()

    asyncio.run(_emit())


if __name__ == "__main__":
    app()
