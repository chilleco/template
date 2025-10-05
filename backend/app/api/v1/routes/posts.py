"""Post CRUD endpoints with RBAC guards."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user, permission_required
from app.db.session import get_session
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate, PostPublic, PostUpdate

router = APIRouter()


@router.get("", response_model=list[PostPublic])
async def list_posts(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Post))
    return list(result.scalars().all())


@router.post("", response_model=PostPublic, status_code=status.HTTP_201_CREATED, dependencies=[Depends(permission_required("posts.create"))])
async def create_post(payload: PostCreate, session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    post = Post(**payload.model_dump(), author_id=current_user.id)
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


@router.get("/{post_id}", response_model=PostPublic)
async def read_post(post_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.put("/{post_id}", response_model=PostPublic, dependencies=[Depends(permission_required("posts.manage"))])
async def update_post(post_id: int, payload: PostUpdate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(post, key, value)
    await session.commit()
    await session.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(permission_required("posts.manage"))])
async def delete_post(post_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    await session.delete(post)
    await session.commit()
    return None
