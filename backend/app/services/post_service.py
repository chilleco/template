from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate, PostRead
from app.repositories.post_repo import PostRepository
from app.db import get_session
from loguru import logger


class PostService:
    def __init__(self):
        self.repo = PostRepository()

    async def create_post(self, data: PostCreate, author_id: int) -> PostRead:
        async for session in get_session():
            post = Post(
                title=data.title,
                content=data.content,
                author_id=author_id
            )
            created = await self.repo.create(session, post)
            logger.info("post.created", post_id=created.id, author_id=author_id)
            return PostRead.from_orm(created)

    async def get_post(self, post_id: int) -> PostRead | None:
        async for session in get_session():
            post = await self.repo.get(session, post_id)
            if not post:
                return None
            return PostRead.from_orm(post)

    async def list_posts(self, skip: int = 0, limit: int = 10) -> List[PostRead]:
        async for session in get_session():
            posts = await self.repo.list(session, skip, limit)
            return [PostRead.from_orm(post) for post in posts]

    async def update_post(self, post_id: int, data: PostUpdate, author_id: int) -> PostRead:
        async for session in get_session():
            post = await self.repo.get(session, post_id)
            if not post:
                raise ValueError("Post not found")
            if post.author_id != author_id:
                raise ValueError("Not authorized to update this post")
            
            update_data = data.model_dump(exclude_unset=True)
            updated = await self.repo.update(session, post, update_data)
            logger.info("post.updated", post_id=post_id, author_id=author_id)
            return PostRead.from_orm(updated)

    async def delete_post(self, post_id: int, author_id: int) -> None:
        async for session in get_session():
            post = await self.repo.get(session, post_id)
            if not post:
                raise ValueError("Post not found")
            if post.author_id != author_id:
                raise ValueError("Not authorized to delete this post")
            
            await self.repo.delete(session, post)
            logger.info("post.deleted", post_id=post_id, author_id=author_id)
