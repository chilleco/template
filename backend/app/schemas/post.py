from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import Field

from app.models.post import PostVisibility
from app.schemas.base import APIModel


class PostBase(APIModel):
    id: uuid.UUID
    title: str
    slug: str
    summary: str | None
    content: str
    locale: str
    visibility: PostVisibility
    is_published: bool
    published_at: datetime | None


class PostCreate(APIModel):
    title: str
    slug: str
    summary: str | None = None
    content: str
    locale: str = "en"
    visibility: PostVisibility = Field(default=PostVisibility.PRIVATE)
    publish: bool = False


class PostUpdate(APIModel):
    slug: str
    title: str | None = None
    summary: str | None = None
    content: str | None = None
    locale: str | None = None
    visibility: PostVisibility | None = None
    publish: bool | None = None


class PostRead(PostBase):
    author_id: uuid.UUID | None


class PostListResponse(APIModel):
    items: list[PostRead]
    meta: PaginationMeta
