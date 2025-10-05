from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post, PostVisibility
from app.models.user import User
from app.schemas.base import PaginationInput, PaginationMeta
from app.schemas.post import PostCreate, PostRead, PostUpdate
from app.services.access import AccessService


class PostService:
    def __init__(self, session: AsyncSession, actor: User | None = None):
        self.session = session
        self.actor = actor

    async def create_post(self, payload: PostCreate) -> PostRead:
        AccessService(self.actor).ensure("post:create")
        now = datetime.now(timezone.utc)
        post = Post(
            author_id=self.actor.id if self.actor else None,
            title=payload.title,
            slug=payload.slug,
            summary=payload.summary,
            content=payload.content,
            locale=payload.locale,
            visibility=payload.visibility,
            is_published=payload.publish,
            published_at=now if payload.publish else None,
        )
        self.session.add(post)
        await self.session.flush()
        return self._to_schema(post)

    async def update_post(self, payload: PostUpdate) -> PostRead:
        post = await self._get_post_by_slug(payload.slug)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post_not_found")

        AccessService(self.actor).ensure_any({"post:update", "post:publish"})
        if payload.title is not None:
            post.title = payload.title
        if payload.summary is not None:
            post.summary = payload.summary
        if payload.content is not None:
            post.content = payload.content
        if payload.locale is not None:
            post.locale = payload.locale
        if payload.visibility is not None:
            post.visibility = payload.visibility
        if payload.publish is not None:
            if payload.publish and not post.is_published:
                post.is_published = True
                post.published_at = datetime.now(timezone.utc)
            elif not payload.publish:
                post.is_published = False
                post.published_at = None
        await self.session.flush()
        return self._to_schema(post)

    async def list_posts(self, pagination: PaginationInput, include_unpublished: bool = False) -> tuple[list[PostRead], PaginationMeta]:
        limit = min(pagination.limit, 100)
        stmt = select(Post).order_by(Post.created_at.desc()).limit(limit + 1)
        if not include_unpublished:
            stmt = stmt.where(Post.is_published.is_(True))
        results = (await self.session.execute(stmt)).scalars().all()
        next_cursor = None
        if len(results) > limit:
            next_cursor = results[-1].slug
            results = results[:-1]
        return [self._to_schema(post) for post in results], PaginationMeta(next_cursor=next_cursor)

    async def get_post(self, slug: str) -> PostRead:
        post = await self._get_post_by_slug(slug)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post_not_found")
        if not post.is_published:
            AccessService(self.actor).ensure_any({"post:read", "post:update"})
        return self._to_schema(post)

    async def _get_post_by_slug(self, slug: str) -> Post | None:
        return (await self.session.execute(select(Post).where(Post.slug == slug))).scalar_one_or_none()

    @staticmethod
    def _to_schema(post: Post) -> PostRead:
        return PostRead(
            id=post.id,
            author_id=post.author_id,
            title=post.title,
            slug=post.slug,
            summary=post.summary,
            content=post.content,
            locale=post.locale,
            visibility=post.visibility,
            is_published=post.is_published,
            published_at=post.published_at,
        )
