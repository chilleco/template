"""Authentication schemas for request/response validation."""
from pydantic import BaseModel, EmailStr, Field
from app.schemas.user import UserPrivate


# Request Schemas
class LoginEmail(BaseModel):
    """Schema for email/password login."""

    email: EmailStr
    password: str
    session_token: str | None = None  # Anonymous session token to merge


class LoginPhone(BaseModel):
    """Schema for phone/password login."""

    phone: str = Field(..., pattern=r"^\+?[1-9]\d{1,14}$")
    password: str
    session_token: str | None = None


class LoginUsername(BaseModel):
    """Schema for username/password login."""

    username: str = Field(..., min_length=3, max_length=50)
    password: str
    session_token: str | None = None


class RegisterEmail(BaseModel):
    """Schema for email registration."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=100)
    session_token: str | None = None


class RegisterPhone(BaseModel):
    """Schema for phone registration."""

    phone: str = Field(..., pattern=r"^\+?[1-9]\d{1,14}$")
    password: str = Field(..., min_length=8, max_length=100)
    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=100)
    session_token: str | None = None


class RegisterUsername(BaseModel):
    """Schema for username registration."""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr | None = None
    password: str = Field(..., min_length=8, max_length=100)
    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=100)
    session_token: str | None = None


class OAuthLogin(BaseModel):
    """Schema for OAuth login."""

    provider: str = Field(..., pattern="^(google|github)$")
    code: str
    redirect_uri: str
    session_token: str | None = None


class RefreshToken(BaseModel):
    """Schema for token refresh."""

    refresh_token: str


class VerifyEmail(BaseModel):
    """Schema for email verification."""

    code: str = Field(..., min_length=6, max_length=6)


class VerifyPhone(BaseModel):
    """Schema for phone verification."""

    code: str = Field(..., min_length=6, max_length=6)


class RequestPasswordReset(BaseModel):
    """Schema for password reset request."""

    email: EmailStr


class ResetPassword(BaseModel):
    """Schema for password reset."""

    token: str
    new_password: str = Field(..., min_length=8, max_length=100)


# Response Schemas
class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class AuthResponse(BaseModel):
    """Authentication response with user info."""

    user: UserPrivate
    tokens: TokenResponse


class SessionTokenResponse(BaseModel):
    """Anonymous session token response."""

    session_token: str
    expires_at: str


class VerificationSent(BaseModel):
    """Verification code sent response."""

    sent: bool
    message: str


# Common Response
class MessageResponse(BaseModel):
    """Simple message response."""

    message: str
