from __future__ import annotations

import pytest

from app.models.user import Role, RolePermission, User, UserRole
from app.services.access import AccessService


@pytest.mark.asyncio
async def test_access_permissions(db_session):
    role = Role(name="Editor", slug="editor")
    role.permissions.append(RolePermission(permission="post:create"))
    user = User(email="perms@example.com", hashed_password="hash")
    user.roles.append(UserRole(role=role))

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    service = AccessService(user)
    perms = service.user_permissions()
    assert "post:create" in perms
    service.ensure("post:create")
