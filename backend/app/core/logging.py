"""Centralized Loguru setup bridging with standard logging."""

from __future__ import annotations

import logging
import sys
from typing import Any

from loguru import logger

from app.core.config import settings


def configure_logging() -> None:
    """Configure Loguru once per process."""
    if getattr(configure_logging, "_configured", False):
        return

    logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))

    logger.remove()
    logger.add(
        sys.stderr,
        level=settings.log_level,
        backtrace=settings.debug,
        diagnose=settings.debug,
        enqueue=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )

    configure_logging._configured = True


__all__ = ["configure_logging", "logger"]
