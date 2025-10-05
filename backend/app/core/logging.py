from __future__ import annotations

import sys
from contextlib import suppress
from typing import Any

from loguru import logger

from app.core.settings import settings


def configure_logging() -> None:
    with suppress(ValueError):
        logger.remove()

    logger.add(sys.stdout, level=settings.log_level, backtrace=False, diagnose=False)


def get_logger(**kwargs: Any):
    return logger.bind(**kwargs)
