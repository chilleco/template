from __future__ import annotations

from collections.abc import Iterable

from fastapi import HTTPException, status

from app.models.user import Role, User


DEFAULT_PERMISSIONS = {
    "user:create",
    "user:read",
    "user:update",
    "user:ban",
    "post:create",
    "post:read",
    "post:update",
    "post:publish",
    "analytics:view",
    "admin:access",
}


class AccessService:
    def __init__(self, user: User | None = None):
        self.user = user

    @staticmethod
    def permissions_from_roles(roles: Iterable[Role]) -> set[str]:
        permissions: set[str] = set()
        for role in roles:
            for perm in role.permissions:
                permissions.add(perm.permission)
        return permissions

    def user_permissions(self) -> set[str]:
        if not self.user:
            return set()
        perms = self.permissions_from_roles(self.user.roles)
        if self.user.is_superuser:
            perms.update(DEFAULT_PERMISSIONS)
        return perms

    def ensure(self, required: str) -> None:
        if required not in self.user_permissions():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="insufficient_permissions")

    def ensure_any(self, required: Iterable[str]) -> None:
        allowed = self.user_permissions()
        if not any(item in allowed for item in required):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="insufficient_permissions")
