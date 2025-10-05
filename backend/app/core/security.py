from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenSubject:
    ACCESS = "access"
    REFRESH = "refresh"
    PRE_AUTH = "pre_auth"


def _create_token(subject: str, token_type: str, expires_delta: timedelta, data: Dict[str, Any]) -> str:
    payload = {
        "sub": subject,
        "type": token_type,
        "exp": datetime.now(timezone.utc) + expires_delta,
        **data,
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


def create_access_token(subject: str, data: Dict[str, Any] | None = None) -> str:
    return _create_token(
        subject,
        TokenSubject.ACCESS,
        timedelta(minutes=settings.access_token_expire_minutes),
        data or {},
    )


def create_refresh_token(subject: str, data: Dict[str, Any] | None = None) -> str:
    return _create_token(
        subject,
        TokenSubject.REFRESH,
        timedelta(minutes=settings.refresh_token_expire_minutes),
        data or {},
    )


def create_pre_auth_token(session_id: str, data: Dict[str, Any] | None = None) -> str:
    return _create_token(
        session_id,
        TokenSubject.PRE_AUTH,
        timedelta(minutes=settings.pre_auth_token_expire_minutes),
        data or {},
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def decode_token(token: str) -> Dict[str, Any] | None:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    except JWTError:
        return None
