"""Session model for user sessions and anonymous tokens."""
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import uuid4
from sqlalchemy import String, DateTime, ForeignKey, Boolean, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class Session(Base):
    """User session model for both authenticated and anonymous users."""

    __tablename__ = "sessions"

    # Primary key
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    # Session token
    session_token: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )

    # User relationship (nullable for anonymous sessions)
    user_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
    )
    user: Mapped["User | None"] = relationship("User", back_populates="sessions")

    # Session type
    is_anonymous: Mapped[bool] = mapped_column(Boolean, default=True)

    # Session data (for storing anonymous user actions)
    # Stores: cart items, favorites, preferences, etc.
    session_data: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)

    # Device information
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    device_type: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Refresh token for authenticated sessions
    refresh_token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    refresh_token_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

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
    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    # Indexes
    __table_args__ = (
        Index("ix_sessions_user_active", "user_id", "is_active"),
        Index("ix_sessions_token", "session_token"),
        Index("ix_sessions_expires", "expires_at"),
    )

    def __repr__(self) -> str:
        return f"<Session {self.id} user={self.user_id} anonymous={self.is_anonymous}>"

    @property
    def is_expired(self) -> bool:
        """Check if session is expired."""
        return datetime.now(timezone.utc) >= self.expires_at

    @property
    def is_valid(self) -> bool:
        """Check if session is valid (not expired, not revoked, active)."""
        return self.is_active and not self.revoked and not self.is_expired

    def update_activity(self) -> None:
        """Update last activity timestamp."""
        self.last_activity_at = datetime.now(timezone.utc)

    def revoke(self) -> None:
        """Revoke the session."""
        self.revoked = True
        self.revoked_at = datetime.now(timezone.utc)
        self.is_active = False

    def convert_to_authenticated(self, user_id: UUID) -> None:
        """Convert anonymous session to authenticated session."""
        self.user_id = user_id
        self.is_anonymous = False
        self.updated_at = datetime.now(timezone.utc)

    def merge_session_data(self, new_data: dict) -> None:
        """Merge new data into session data."""
        self.session_data.update(new_data)
        self.updated_at = datetime.now(timezone.utc)
