from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_active_user, get_db_session, require_permission
from app.models.user import Role, User, UserRole
from app.schemas.user import RoleRead, UserRead, UserUpdate
from app.services.access import AccessService

router = APIRouter()


def _serialize_user(user: User) -> UserRead:
    permissions = sorted(AccessService(user).user_permissions())
    roles = [role.slug for role in user.roles]
    return UserRead(
        id=user.id,
        email=user.email,
        phone_e164=user.phone_e164,
        username=user.username,
        full_name=user.full_name,
        locale=user.locale,
        timezone=user.timezone,
        is_active=user.is_active,
        is_verified=user.is_verified,
        is_superuser=user.is_superuser,
        banned_until=user.banned_until,
        roles=roles,
        permissions=permissions,
    )


@router.post("/me/profile", response_model=UserRead)
async def read_profile(current_user: User = Depends(get_current_active_user)) -> UserRead:
    return _serialize_user(current_user)


@router.post("/me/update", response_model=UserRead)
async def update_profile(
    payload: UserUpdate,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
) -> UserRead:
    if payload.full_name is not None:
        current_user.full_name = payload.full_name
    if payload.locale is not None:
        current_user.locale = payload.locale
    if payload.timezone is not None:
        current_user.timezone = payload.timezone
    await session.flush()
    return _serialize_user(current_user)


@router.post("/roles/list", response_model=list[RoleRead])
async def list_roles(
    _: User = Depends(require_permission("admin:access")),
    session: AsyncSession = Depends(get_db_session),
) -> list[RoleRead]:
    roles = (await session.execute(select(Role))).scalars().unique().all()
    return [
        RoleRead(
            name=role.name,
            slug=role.slug,
            permissions=[perm.permission for perm in role.permissions],
        )
        for role in roles
    ]


@router.post("/ban", response_model=UserRead)
async def ban_user(
    payload: dict,
    _: User = Depends(require_permission("user:ban")),
    session: AsyncSession = Depends(get_db_session),
) -> UserRead:
    user_id_str = payload.get("user_id")
    duration_minutes = payload.get("minutes")
    if not user_id_str or duration_minutes is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid_payload")
    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid_user_id") from exc

    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user_not_found")

    user.banned_until = datetime.now(timezone.utc) + timedelta(minutes=int(duration_minutes))
    await session.flush()
    return _serialize_user(user)


@router.post("/roles/assign", response_model=UserRead)
async def assign_role(
    payload: dict,
    _: User = Depends(require_permission("admin:access")),
    session: AsyncSession = Depends(get_db_session),
) -> UserRead:
    user_id = payload.get("user_id")
    role_slug = payload.get("role_slug")
    if not user_id or not role_slug:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid_payload")
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid_user_id") from exc

    user = await session.get(User, user_uuid)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user_not_found")

    role = (await session.execute(select(Role).where(Role.slug == role_slug))).scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="role_not_found")

    existing = (
        await session.execute(
            select(UserRole).where(UserRole.user_id == user.id, UserRole.role_id == role.id)
        )
    ).scalar_one_or_none()
    if not existing:
        session.add(UserRole(user_id=user.id, role_id=role.id))
        await session.flush()
    return _serialize_user(user)
