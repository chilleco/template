from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.post import Post
from app.db import get_session


class PostRepository:
    def __init__(self):
        pass

    async def create(self, session: AsyncSession, post: Post) -> Post:
        session.add(post)
        await session.commit()
        await session.refresh(post)
        return post

    async def get(self, session: AsyncSession, post_id: int) -> Optional[Post]:
        result = await session.execute(
            select(Post).options(selectinload(Post.author)).where(Post.id == post_id)
        )
        return result.scalar_one_or_none()

    async def list(self, session: AsyncSession, skip: int = 0, limit: int = 10) -> List[Post]:
        result = await session.execute(
            select(Post)
            .options(selectinload(Post.author))
            .offset(skip)
            .limit(limit)
            .order_by(Post.created_at.desc())
        )
        return result.scalars().all()

    async def update(self, session: AsyncSession, post: Post, data: dict) -> Post:
        for key, value in data.items():
            setattr(post, key, value)
        await session.commit()
        await session.refresh(post)
        return post

    async def delete(self, session: AsyncSession, post: Post) -> None:
        await session.delete(post)
        await session.commit()
