from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session, get_pre_auth_session
from app.schemas.user import (
    AuthResponse,
    PreAuthState,
    SessionBootstrapRequest,
    SessionState,
    TokenPair,
    TokenRefreshRequest,
    UserCreatePassword,
    UserLoginPassword,
)
from app.services.auth import AuthService

router = APIRouter()


@router.post("/session/bootstrap", response_model=SessionState)
async def bootstrap_session(
    payload: SessionBootstrapRequest | None = None,
    session: AsyncSession = Depends(get_db_session),
) -> SessionState:
    service = AuthService(session)
    payload = payload or SessionBootstrapRequest()
    pre_auth = await service.ensure_pre_auth_session(payload.token, data=payload.data)
    return SessionState(token=pre_auth.token, expires_at=pre_auth.expires_at, data=pre_auth.data)


@router.post("/register/password", response_model=AuthResponse)
async def register_with_password(
    payload: UserCreatePassword,
    session_state: PreAuthState = Depends(get_pre_auth_session),
    session: AsyncSession = Depends(get_db_session),
) -> AuthResponse:
    service = AuthService(session)
    await service.bootstrap_default_roles()
    return await service.register_local_user(
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
        session_token=session_state.token,
    )


@router.post("/login/password", response_model=AuthResponse)
async def login_with_password(
    payload: UserLoginPassword,
    session_state: PreAuthState = Depends(get_pre_auth_session),
    session: AsyncSession = Depends(get_db_session),
) -> AuthResponse:
    service = AuthService(session)
    return await service.authenticate_local(
        email=payload.email,
        password=payload.password,
        session_token=session_state.token,
    )


@router.post("/token/refresh", response_model=TokenPair)
async def refresh_token(
    payload: TokenRefreshRequest,
    session: AsyncSession = Depends(get_db_session),
) -> TokenPair:
    service = AuthService(session)
    return await service.rotate_tokens(payload.refresh_token)
