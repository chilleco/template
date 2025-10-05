"""Logging configuration with loguru and Sentry integration."""
import sys
from pathlib import Path
from loguru import logger
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from app.core.config import settings


def setup_logging() -> None:
    """Configure loguru logger with appropriate settings."""
    # Remove default handler
    logger.remove()

    # Console handler - colored output for development
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    logger.add(
        sys.stdout,
        format=log_format,
        level="DEBUG" if settings.DEBUG else "INFO",
        colorize=True,
        backtrace=True,
        diagnose=settings.DEBUG,
    )

    # File handler - rotating file logs
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logger.add(
        log_dir / "app_{time:YYYY-MM-DD}.log",
        format=log_format,
        level="INFO",
        rotation="00:00",  # Rotate at midnight
        retention="30 days",
        compression="zip",
        backtrace=True,
        diagnose=True,
    )

    # Error file handler - separate file for errors
    logger.add(
        log_dir / "error_{time:YYYY-MM-DD}.log",
        format=log_format,
        level="ERROR",
        rotation="00:00",
        retention="90 days",
        compression="zip",
        backtrace=True,
        diagnose=True,
    )

    logger.info(f"Logging initialized for environment: {settings.ENVIRONMENT}")


def setup_sentry() -> None:
    """Configure Sentry for error tracking."""
    if not settings.SENTRY_DSN:
        logger.warning("Sentry DSN not configured, skipping Sentry initialization")
        return

    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        release=f"{settings.APP_NAME}@{settings.APP_VERSION}",
        integrations=[
            FastApiIntegration(transaction_style="endpoint"),
            SqlalchemyIntegration(),
            RedisIntegration(),
        ],
        # Performance monitoring
        traces_sample_rate=1.0 if settings.ENVIRONMENT == "local" else 0.1,
        # Error sampling
        sample_rate=1.0,
        # Send PII data
        send_default_pii=False,
        # Attach stacktrace
        attach_stacktrace=True,
        # Max breadcrumbs
        max_breadcrumbs=50,
        # Request bodies
        max_request_body_size="medium",
        # Before send callback
        before_send=before_send_sentry,
    )

    logger.info(f"Sentry initialized for environment: {settings.ENVIRONMENT}")


def before_send_sentry(event: dict, hint: dict) -> dict | None:
    """
    Filter and modify events before sending to Sentry.

    Args:
        event: Sentry event
        hint: Event hint with exception info

    Returns:
        Modified event or None to skip
    """
    # Skip certain exceptions
    if "exc_info" in hint:
        exc_type, exc_value, tb = hint["exc_info"]

        # Skip HTTP 404 errors
        if exc_type.__name__ == "ResourceNotFoundError":
            return None

    # Remove sensitive data
    if "request" in event:
        request = event["request"]

        # Remove sensitive headers
        if "headers" in request:
            sensitive_headers = ["authorization", "cookie", "x-api-key"]
            for header in sensitive_headers:
                if header in request["headers"]:
                    request["headers"][header] = "[REDACTED]"

        # Remove sensitive data from body
        if "data" in request and isinstance(request["data"], dict):
            sensitive_fields = ["password", "token", "secret", "api_key"]
            for field in sensitive_fields:
                if field in request["data"]:
                    request["data"][field] = "[REDACTED]"

    return event


def log_exception(exc: Exception, **extra: dict) -> None:
    """
    Log exception with context to loguru and Sentry.

    Args:
        exc: Exception to log
        **extra: Additional context
    """
    logger.exception(f"Exception occurred: {str(exc)}", extra=extra)

    if settings.SENTRY_DSN:
        sentry_sdk.capture_exception(exc, extra=extra)
