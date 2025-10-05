from __future__ import annotations

import uuid
from datetime import datetime
from typing import Literal

from pydantic import EmailStr, Field

from app.schemas.base import APIModel


class UserBase(APIModel):
    id: uuid.UUID
    email: EmailStr | None
    phone_e164: str | None
    username: str | None
    full_name: str | None
    locale: str
    timezone: str
    is_active: bool
    is_verified: bool
    is_superuser: bool
    banned_until: datetime | None


class UserRead(UserBase):
    roles: list[str] = Field(default_factory=list)
    permissions: list[str] = Field(default_factory=list)


class UserCreatePassword(APIModel):
    email: EmailStr
    password: str
    full_name: str | None = None


class UserLoginPassword(APIModel):
    email: EmailStr
    password: str


class UserCreateOAuth(APIModel):
    provider: str
    provider_token: str
    email: EmailStr | None = None


class UserCreatePhone(APIModel):
    phone_e164: str
    otp_code: str


class UserUpdate(APIModel):
    full_name: str | None = None
    locale: str | None = None
    timezone: str | None = None


class TokenPair(APIModel):
    access_token: str
    refresh_token: str
    token_type: Literal["bearer"] = "bearer"


class TokenRefreshRequest(APIModel):
    refresh_token: str


class SessionState(APIModel):
    token: str
    expires_at: datetime
    data: dict = Field(default_factory=dict)

class SessionBootstrapRequest(APIModel):
    token: str | None = None
    data: dict = Field(default_factory=dict)


class AuthResponse(APIModel):
    user: UserRead
    tokens: TokenPair
    session: SessionState


class PreAuthState(APIModel):
    token: str
    expires_at: datetime
    data: dict = Field(default_factory=dict)


class ProviderLink(APIModel):
    provider: str
    authorize_url: str


class AccessRule(APIModel):
    slug: str
    description: str


class RoleRead(APIModel):
    name: str
    slug: str
    permissions: list[str]
