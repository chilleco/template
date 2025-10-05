"""Role-based access control service."""

from __future__ import annotations

from fastapi import Depends

from app.models.user import User, UserRole


ROLE_HIERARCHY: dict[UserRole, set[str]] = {
    UserRole.SUPERADMIN: {"*"},
    UserRole.ADMIN: {"users.manage", "posts.manage", "analytics.view", "admin.access"},
    UserRole.EDITOR: {"posts.manage", "analytics.view"},
    UserRole.CREATOR: {"posts.create", "posts.manage_own"},
    UserRole.USER: {"posts.read", "profile.manage"},
    UserRole.RESTRICTED: {"posts.read"},
}


class PermissionService:
    def __init__(self) -> None:
        pass

    async def has_permission(self, user: User, permission: str) -> bool:
        allowed = ROLE_HIERARCHY.get(user.role, set())
        return "*" in allowed or permission in allowed


async def get_permission_service() -> PermissionService:
    return PermissionService()
