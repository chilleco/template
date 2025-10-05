"""User-facing schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.models.user import AuthProvider, UserRole, UserStatus
from app.schemas.common import TimestampedSchema


class UserBase(BaseModel):
    id: int
    email: EmailStr | None = None
    phone: str | None = None
    username: str | None = None
    role: UserRole
    status: UserStatus
    is_email_verified: bool
    is_phone_verified: bool
    locale: str | None = Field(None, description="Preferred locale code")
    profile: dict
    settings: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserPublic(UserBase):
    pass


class UserCreatePassword(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    username: str | None = None


class UserCreatePhone(BaseModel):
    phone: str = Field(min_length=8, max_length=32)
    code: str = Field(min_length=4, max_length=8)
    username: str | None = None


class UserLogin(BaseModel):
    identifier: str
    password: str | None = None
    provider: AuthProvider = AuthProvider.PASSWORD


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class SessionSnapshot(BaseModel):
    snapshot_id: str
    expires_in: int
    payload: dict


class TokenRefresh(BaseModel):
    refresh_token: str
