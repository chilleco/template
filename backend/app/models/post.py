"""Post model with access control and moderation."""
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import uuid4
from sqlalchemy import String, Text, DateTime, Boolean, ForeignKey, Index, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class PostStatus(str, Enum):
    """Post status for moderation and publishing."""

    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    MODERATED = "moderated"  # Hidden by moderator


class Post(Base):
    """Post model with author attribution and access control."""

    __tablename__ = "posts"

    # Primary key
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    # Content
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(300), unique=True, index=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    excerpt: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # SEO
    meta_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    meta_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    meta_keywords: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Media
    cover_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Status & Publishing
    status: Mapped[PostStatus] = mapped_column(
        SQLEnum(PostStatus, name="post_status"),
        default=PostStatus.DRAFT,
        nullable=False,
    )
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Author relationship
    author_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    author: Mapped["User"] = relationship("User", back_populates="posts")

    # Moderation
    moderated_by: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    moderation_reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    moderated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Engagement metrics
    views_count: Mapped[int] = mapped_column(default=0)
    likes_count: Mapped[int] = mapped_column(default=0)
    comments_count: Mapped[int] = mapped_column(default=0)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Indexes for common queries
    __table_args__ = (
        Index("ix_posts_author_status", "author_id", "status"),
        Index("ix_posts_status_published", "status", "published_at"),
        Index("ix_posts_created_at", "created_at"),
        Index("ix_posts_slug", "slug"),
    )

    def __repr__(self) -> str:
        return f"<Post {self.id} {self.title[:50]}>"

    @property
    def is_published(self) -> bool:
        """Check if post is published and visible."""
        return (
            self.status == PostStatus.PUBLISHED
            and self.published_at is not None
            and self.published_at <= datetime.now(timezone.utc)
        )

    def publish(self) -> None:
        """Publish the post."""
        self.status = PostStatus.PUBLISHED
        if not self.published_at:
            self.published_at = datetime.now(timezone.utc)

    def unpublish(self) -> None:
        """Unpublish the post (move to draft)."""
        self.status = PostStatus.DRAFT

    def archive(self) -> None:
        """Archive the post."""
        self.status = PostStatus.ARCHIVED

    def moderate(self, moderator_id: UUID, reason: str) -> None:
        """Mark post as moderated."""
        self.status = PostStatus.MODERATED
        self.moderated_by = moderator_id
        self.moderation_reason = reason
        self.moderated_at = datetime.now(timezone.utc)

    def increment_views(self) -> None:
        """Increment view counter."""
        self.views_count += 1
