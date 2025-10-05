"""Custom exceptions and error handling."""
from typing import Any
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from loguru import logger


class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


# Authentication & Authorization Exceptions
class AuthenticationError(AppException):
    """Authentication failed."""

    def __init__(self, message: str = "Authentication failed", details: dict[str, Any] | None = None) -> None:
        super().__init__(
            code="AUTHENTICATION_ERROR",
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details,
        )


class AuthorizationError(AppException):
    """Permission denied."""

    def __init__(self, message: str = "Permission denied", details: dict[str, Any] | None = None) -> None:
        super().__init__(
            code="AUTHORIZATION_ERROR",
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            details=details,
        )


class InvalidTokenError(AppException):
    """Invalid or expired token."""

    def __init__(self, message: str = "Invalid or expired token", details: dict[str, Any] | None = None) -> None:
        super().__init__(
            code="INVALID_TOKEN",
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details,
        )


# Resource Exceptions
class ResourceNotFoundError(AppException):
    """Resource not found."""

    def __init__(self, resource: str, identifier: str | None = None) -> None:
        details = {"resource": resource}
        if identifier:
            details["identifier"] = identifier

        super().__init__(
            code="RESOURCE_NOT_FOUND",
            message=f"{resource} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            details=details,
        )


class ResourceAlreadyExistsError(AppException):
    """Resource already exists."""

    def __init__(self, resource: str, field: str, value: str) -> None:
        super().__init__(
            code="RESOURCE_ALREADY_EXISTS",
            message=f"{resource} with {field}={value} already exists",
            status_code=status.HTTP_409_CONFLICT,
            details={"resource": resource, "field": field, "value": value},
        )


# Validation Exceptions
class ValidationError(AppException):
    """Validation failed."""

    def __init__(self, message: str, field: str | None = None, details: dict[str, Any] | None = None) -> None:
        error_details = details or {}
        if field:
            error_details["field"] = field

        super().__init__(
            code="VALIDATION_ERROR",
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=error_details,
        )


# Business Logic Exceptions
class BusinessLogicError(AppException):
    """Business logic constraint violated."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(
            code="BUSINESS_LOGIC_ERROR",
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details,
        )


# Rate Limiting
class RateLimitExceededError(AppException):
    """Rate limit exceeded."""

    def __init__(self, retry_after: int | None = None) -> None:
        details = {}
        if retry_after:
            details["retry_after"] = retry_after

        super().__init__(
            code="RATE_LIMIT_EXCEEDED",
            message="Too many requests",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            details=details,
        )


# External Services
class ExternalServiceError(AppException):
    """External service error."""

    def __init__(self, service: str, message: str, details: dict[str, Any] | None = None) -> None:
        error_details = details or {}
        error_details["service"] = service

        super().__init__(
            code="EXTERNAL_SERVICE_ERROR",
            message=f"{service} error: {message}",
            status_code=status.HTTP_502_BAD_GATEWAY,
            details=error_details,
        )


# Exception Handlers
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    Handle AppException and return standardized error response.

    Args:
        request: FastAPI request
        exc: Application exception

    Returns:
        JSON error response
    """
    logger.error(
        f"AppException: {exc.code} - {exc.message}",
        extra={
            "code": exc.code,
            "status_code": exc.status_code,
            "details": exc.details,
            "path": request.url.path,
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            },
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle HTTPException and return standardized error response.

    Args:
        request: FastAPI request
        exc: HTTP exception

    Returns:
        JSON error response
    """
    logger.error(
        f"HTTPException: {exc.status_code} - {exc.detail}",
        extra={
            "status_code": exc.status_code,
            "detail": exc.detail,
            "path": request.url.path,
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "HTTP_ERROR",
                "message": exc.detail,
                "details": {},
            },
        },
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle unexpected exceptions.

    Args:
        request: FastAPI request
        exc: General exception

    Returns:
        JSON error response
    """
    logger.exception(
        f"Unhandled exception: {str(exc)}",
        extra={"path": request.url.path},
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
                "details": {},
            },
        },
    )
