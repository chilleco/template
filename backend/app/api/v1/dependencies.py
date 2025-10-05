"""Reusable dependency overrides for API routes."""

from __future__ import annotations

from fastapi import Depends, HTTPException, status

from app.services.auth import AuthService, get_auth_service
from app.services.permissions import PermissionService, get_permission_service


async def get_current_user(auth_service: AuthService = Depends(get_auth_service)):
    user = await auth_service.get_current_user()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user


def permission_required(permission: str):
    async def _dependency(
        user=Depends(get_current_user),
        permission_service: PermissionService = Depends(get_permission_service),
    ):
        if not await permission_service.has_permission(user, permission):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user

    return _dependency


__all__ = ["get_current_user", "permission_required"]
