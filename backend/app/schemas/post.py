"""Post schemas for request/response validation."""
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from app.models.post import PostStatus


# Request Schemas
class PostCreate(BaseModel):
    """Schema for creating a new post."""

    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    excerpt: str | None = Field(None, max_length=500)
    cover_image_url: str | None = Field(None, max_length=500)
    meta_title: str | None = Field(None, max_length=255)
    meta_description: str | None = Field(None, max_length=500)
    meta_keywords: str | None = Field(None, max_length=255)
    status: PostStatus = PostStatus.DRAFT
    is_featured: bool = False


class PostUpdate(BaseModel):
    """Schema for updating a post."""

    title: str | None = Field(None, min_length=1, max_length=255)
    content: str | None = Field(None, min_length=1)
    excerpt: str | None = Field(None, max_length=500)
    cover_image_url: str | None = Field(None, max_length=500)
    meta_title: str | None = Field(None, max_length=255)
    meta_description: str | None = Field(None, max_length=500)
    meta_keywords: str | None = Field(None, max_length=255)
    status: PostStatus | None = None
    is_featured: bool | None = None


class PostPublish(BaseModel):
    """Schema for publishing a post."""

    publish: bool = True


class PostModerate(BaseModel):
    """Schema for moderating a post."""

    reason: str = Field(..., min_length=1, max_length=500)


# Response Schemas
class PostAuthor(BaseModel):
    """Post author info."""

    id: UUID
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    avatar_url: str | None = None

    model_config = {"from_attributes": True}


class PostBase(BaseModel):
    """Base post schema."""

    id: UUID
    title: str
    slug: str
    excerpt: str | None = None
    cover_image_url: str | None = None
    status: PostStatus
    is_featured: bool
    views_count: int
    likes_count: int
    comments_count: int
    created_at: datetime
    updated_at: datetime
    published_at: datetime | None = None

    model_config = {"from_attributes": True}


class PostPublic(PostBase):
    """Public post with author info."""

    author: PostAuthor

    model_config = {"from_attributes": True}


class PostDetail(PostPublic):
    """Detailed post with full content."""

    content: str
    meta_title: str | None = None
    meta_description: str | None = None
    meta_keywords: str | None = None

    model_config = {"from_attributes": True}


class PostList(BaseModel):
    """Post list response."""

    posts: list[PostPublic]
    total: int
    page: int
    size: int


# Filter/Search Schemas
class PostFilters(BaseModel):
    """Post list filters."""

    status: PostStatus | None = None
    author_id: UUID | None = None
    is_featured: bool | None = None
    search: str | None = Field(None, max_length=255)
