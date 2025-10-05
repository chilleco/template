from __future__ import annotations

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from app.core.settings import settings


def configure_sentry() -> None:
    if not settings.sentry_dsn:
        return

    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=0.2,
        enable_tracing=True,
        integrations=[FastApiIntegration(transaction_style="endpoint"), SqlalchemyIntegration(), RedisIntegration()],
        environment=settings.app_env,
    )
