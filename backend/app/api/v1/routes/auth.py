"""Authentication endpoints supporting multi-stage flows."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.user import SessionSnapshot, TokenPair, TokenRefresh, UserCreatePassword, UserLogin, UserPublic
from app.services.auth import AuthError, AuthService, get_auth_service

router = APIRouter(prefix="/auth")


@router.post("/register/password", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register_password_user(payload: UserCreatePassword, service: AuthService = Depends(get_auth_service)):
    try:
        user = await service.register_password_user(payload)
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return user


@router.post("/login", response_model=TokenPair)
async def login(payload: UserLogin, service: AuthService = Depends(get_auth_service)):
    try:
        return await service.authenticate(payload)
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/refresh", response_model=TokenPair)
async def refresh(payload: TokenRefresh, service: AuthService = Depends(get_auth_service)):
    try:
        return await service.refresh(payload)
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.post("/snapshot", response_model=SessionSnapshot)
async def snapshot_session(data: dict, service: AuthService = Depends(get_auth_service)):
    return await service.snapshot_session(data)
