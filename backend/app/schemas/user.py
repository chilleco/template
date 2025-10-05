"""User schemas for request/response validation."""
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.core.permissions import Role


# Request Schemas
class UserCreate(BaseModel):
    """Schema for creating a new user."""

    email: EmailStr | None = None
    phone: str | None = None
    username: str | None = None
    password: str = Field(..., min_length=8, max_length=100)
    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=100)
    locale: str = "en"

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v

    @field_validator("email", "phone", "username")
    @classmethod
    def validate_identifier(cls, v: str | None, info) -> str | None:
        """Ensure at least one identifier is provided."""
        return v


class UserUpdate(BaseModel):
    """Schema for updating user profile."""

    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=100)
    bio: str | None = Field(None, max_length=500)
    avatar_url: str | None = Field(None, max_length=500)
    locale: str | None = Field(None, pattern="^(en|ru|es|zh|ar)$")
    timezone: str | None = None
    theme: str | None = Field(None, pattern="^(light|dark|system)$")


class UserPasswordUpdate(BaseModel):
    """Schema for updating user password."""

    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserBan(BaseModel):
    """Schema for banning a user."""

    reason: str = Field(..., min_length=1, max_length=500)
    duration_days: int | None = Field(None, ge=1)


# Response Schemas
class UserBase(BaseModel):
    """Base user schema."""

    id: UUID
    email: str | None = None
    phone: str | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    avatar_url: str | None = None
    bio: str | None = None
    role: Role
    locale: str
    timezone: str
    theme: str
    email_verified: bool
    phone_verified: bool
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserPublic(BaseModel):
    """Public user profile (limited fields)."""

    id: UUID
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    avatar_url: str | None = None
    bio: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class UserPrivate(UserBase):
    """Private user profile (full fields for authenticated user)."""

    is_banned: bool
    banned_until: datetime | None = None
    last_login_at: datetime | None = None
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserList(BaseModel):
    """User list response."""

    users: list[UserBase]
    total: int
    page: int
    size: int


# Filter/Pagination Schemas
class UserFilters(BaseModel):
    """User list filters."""

    role: Role | None = None
    is_active: bool | None = None
    is_banned: bool | None = None
    search: str | None = Field(None, max_length=255)


class PaginationParams(BaseModel):
    """Pagination parameters."""

    page: int = Field(1, ge=1)
    size: int = Field(20, ge=1, le=100)
