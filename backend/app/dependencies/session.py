from __future__ import annotations

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db_session
from app.schemas.user import PreAuthState
from app.services.auth import AuthService


async def get_pre_auth_session(
    session: AsyncSession = Depends(get_db_session),
    pre_auth_token: str | None = Header(default=None, alias="X-Pre-Auth-Token"),
) -> PreAuthState:
    service = AuthService(session)
    return await service.ensure_pre_auth_session(pre_auth_token)
