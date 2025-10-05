"""Post schemas used for CRUD operations."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.models.post import PostStatus, PostVisibility


class PostBase(BaseModel):
    title: str
    summary: str | None = None
    content: str
    visibility: PostVisibility = PostVisibility.PUBLIC
    status: PostStatus = PostStatus.DRAFT
    locale: str = Field(default="en", min_length=2, max_length=10)
    seo: dict = Field(default_factory=dict)
    extra: dict = Field(default_factory=dict)
    is_featured: bool = False


class PostCreate(PostBase):
    slug: str = Field(min_length=3, max_length=255)


class PostUpdate(BaseModel):
    title: str | None = None
    summary: str | None = None
    content: str | None = None
    visibility: PostVisibility | None = None
    status: PostStatus | None = None
    locale: str | None = None
    seo: dict | None = None
    extra: dict | None = None
    is_featured: bool | None = None


class PostPublic(PostBase):
    id: int
    slug: str
    author_id: int
    published_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
