"""Loguru + Sentry sink."""

import sys
from loguru import logger
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from app.core.settings import get_settings

settings = get_settings()

# ---------- 1. Loguru baseline ---------- #
logger.remove()                          # убираем дефолтный sink
logger.add(
    sys.stdout,
    level=settings.log_level,
    backtrace=True,
    diagnose=False,                      # отключаем тяжёлую трассировку в проде
    serialize=True,                      # JSON-формат → удобно парсить в Loki/ELK
)

# ---------- 2. Sentry integration ---------- #
if settings.sentry_dsn:
    sentry_logging = LoggingIntegration(
        level="WARNING",      # всё ≥ WARNING уходит в Sentry как breadcrumbs
        event_level="ERROR",  # ERROR/CRITICAL → полноценные events
    )
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.env,
        traces_sample_rate=settings.sentry_sample_rate,
        integrations=[sentry_logging],
    )

    # Доп. sink: прокидываем Loguru-записи в sentry_sdk.capture_message
    def _sentry_sink(message):
        record = message.record
        sentry_sdk.capture_message(
            record["message"],
            level=record["level"].name.lower(),
        )

    logger.add(_sentry_sink, level="CRITICAL")  # кастом: критика сразу идёт как alert
