from __future__ import annotations

import uuid
from typing import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import TokenSubject, decode_token
from app.dependencies.database import get_db_session
from app.models.user import User
from app.services.access import AccessService

security = HTTPBearer(auto_error=False)


def _parse_authorization(credentials: HTTPAuthorizationCredentials | None) -> str:
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not_authenticated")
    return credentials.credentials


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    session: AsyncSession = Depends(get_db_session),
) -> User:
    token = _parse_authorization(credentials)
    payload = decode_token(token)
    if not payload or payload.get("type") != TokenSubject.ACCESS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_token")

    try:
        user_id = uuid.UUID(payload["sub"])
    except (ValueError, KeyError) as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_token") from exc

    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user_not_found")
    return user


async def get_current_active_user(user: User = Depends(get_current_user)) -> User:
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user_inactive")
    return user


def require_permission(permission: str) -> Callable[[User], User]:
    def dependency(user: User = Depends(get_current_active_user)) -> User:
        AccessService(user).ensure(permission)
        return user

    return dependency


async def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    session: AsyncSession = Depends(get_db_session),
) -> User | None:
    if not credentials or credentials.scheme.lower() != "bearer":
        return None
    payload = decode_token(credentials.credentials)
    if not payload or payload.get("type") != TokenSubject.ACCESS:
        return None
    try:
        user_id = uuid.UUID(payload["sub"])
    except (ValueError, KeyError):
        return None
    return await session.get(User, user_id)
