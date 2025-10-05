"""User resource endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user, permission_required
from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserPublic

router = APIRouter()


@router.get("/me", response_model=UserPublic)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserPublic, dependencies=[Depends(permission_required("users.manage"))])
async def read_user(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("", response_model=list[UserPublic], dependencies=[Depends(permission_required("users.manage"))])
async def list_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    return list(result.scalars().all())
