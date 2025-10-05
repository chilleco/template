"""Sentry integration for unified error reporting."""

from __future__ import annotations

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from app.core.config import settings


def configure_sentry() -> None:
    if not settings.sentry_dsn or getattr(configure_sentry, "_configured", False):
        return

    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=0.2,
        profiles_sample_rate=0.1,
        environment="development" if settings.debug else "production",
        integrations=[
            FastApiIntegration(transaction_style="endpoint"),
            SqlalchemyIntegration(),
            LoggingIntegration(event_level="ERROR"),
        ],
    )
    configure_sentry._configured = True


__all__ = ["configure_sentry"]
