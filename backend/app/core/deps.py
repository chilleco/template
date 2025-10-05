"""FastAPI dependencies for authentication and authorization."""
from typing import Annotated
from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import decode_token, verify_token_type
from app.core.exceptions import AuthenticationError, InvalidTokenError
from app.models.user import User
from app.models.session import Session


async def get_current_user_optional(
    authorization: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_db),
) -> User | None:
    """
    Get current authenticated user (optional).

    Returns None if no valid token provided.

    Args:
        authorization: Authorization header
        db: Database session

    Returns:
        User or None
    """
    if not authorization:
        return None

    if not authorization.startswith("Bearer "):
        return None

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)

    if not payload:
        return None

    if not verify_token_type(payload, "access"):
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    # Get user from database
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    return user


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Get current authenticated user (required).

    Raises exception if no valid token provided.

    Args:
        authorization: Authorization header
        db: Database session

    Returns:
        User

    Raises:
        AuthenticationError: If authentication fails
    """
    if not authorization:
        raise AuthenticationError("Missing authorization header")

    if not authorization.startswith("Bearer "):
        raise AuthenticationError("Invalid authorization header format")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)

    if not payload:
        raise InvalidTokenError()

    if not verify_token_type(payload, "access"):
        raise InvalidTokenError("Invalid token type")

    user_id = payload.get("sub")
    if not user_id:
        raise InvalidTokenError("Invalid token payload")

    # Get user from database
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise AuthenticationError("User not found")

    if not user.is_active:
        raise AuthenticationError("User account is inactive")

    if user.is_banned:
        raise AuthenticationError("User account is banned")

    return user


async def get_session_token(
    x_session_token: Annotated[str | None, Header()] = None,
) -> str | None:
    """
    Get session token from header.

    Args:
        x_session_token: Session token header

    Returns:
        Session token or None
    """
    return x_session_token


async def get_or_create_session(
    session_token: str | None = Depends(get_session_token),
    db: AsyncSession = Depends(get_db),
) -> Session:
    """
    Get or create anonymous session.

    Args:
        session_token: Session token from header
        db: Database session

    Returns:
        Session instance
    """
    from datetime import datetime, timedelta, timezone
    from app.core.security import create_session_token

    # If session token provided, try to get existing session
    if session_token:
        result = await db.execute(
            select(Session).where(
                Session.session_token == session_token,
                Session.is_active == True,  # noqa: E712
                Session.revoked == False,  # noqa: E712
            )
        )
        session = result.scalar_one_or_none()

        if session and not session.is_expired:
            session.update_activity()
            await db.commit()
            return session

    # Create new anonymous session
    new_token = create_session_token()
    new_session = Session(
        session_token=new_token,
        is_anonymous=True,
        expires_at=datetime.now(timezone.utc)
        + timedelta(days=settings.SESSION_TOKEN_EXPIRE_DAYS),
    )

    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)

    return new_session


# Import settings
from app.core.config import settings
