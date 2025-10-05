"""Authentication and session orchestration services."""

from __future__ import annotations

import json
import uuid
from datetime import timedelta

from fastapi import Depends, Request
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.redis import get_redis
from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
)
from app.db.session import get_session
from app.models.user import AuthProvider, User, UserRole, UserStatus
from app.schemas.user import (
    SessionSnapshot,
    TokenPair,
    TokenRefresh,
    UserCreatePassword,
    UserLogin,
)
from app.tasks.registry import task_registry


SNAPSHOT_PREFIX = "session:snapshot"
REFRESH_TOKEN_PREFIX = "session:refresh"


class AuthError(Exception):
    pass


class AuthService:
    def __init__(
        self,
        request: Request,
        session: AsyncSession,
        redis: Redis,
    ) -> None:
        self.request = request
        self.session = session
        self.redis = redis

    async def register_password_user(self, payload: UserCreatePassword) -> User:
        user = User(
            email=payload.email.lower(),
            username=payload.username,
            hashed_password=get_password_hash(payload.password),
            status=UserStatus.ACTIVE,
            role=UserRole.USER,
            profile={"locale": settings.default_locale},
            settings={"notifications": True},
        )
        self.session.add(user)
        try:
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            raise AuthError("User already exists") from exc
        await self.session.refresh(user)
        await task_registry.emit("user.registered", {"user_id": user.id})
        return user

    async def authenticate(self, payload: UserLogin) -> TokenPair:
        identifier = payload.identifier.lower()
        stmt = select(User).where(
            (User.email == identifier) | (User.username == identifier) | (User.phone == identifier)
        )
        result = await self.session.execute(stmt)
        user: User | None = result.scalars().first()
        if not user:
            raise AuthError("User not found")

        if payload.provider == AuthProvider.PASSWORD:
            if not user.hashed_password or not payload.password:
                raise AuthError("Password required")
            if not verify_password(payload.password, user.hashed_password):
                raise AuthError("Invalid credentials")

        if user.status != UserStatus.ACTIVE:
            raise AuthError(f"User is {user.status}")

        token_pair = await self._issue_tokens(str(user.id))
        return token_pair

    async def refresh(self, payload: TokenRefresh) -> TokenPair:
        try:
            payload_data = decode_token(payload.refresh_token)
        except ValueError as exc:  # noqa: TRY003
            raise AuthError("Invalid refresh token") from exc

        if payload_data.get("type") != "refresh":
            raise AuthError("Invalid token type")

        stored = await self.redis.get(f"{REFRESH_TOKEN_PREFIX}:{payload.refresh_token}")
        if stored != payload.refresh_token:
            raise AuthError("Refresh token revoked")

        subject = payload_data["sub"]
        return await self._issue_tokens(subject)

    async def get_current_user(self) -> User | None:
        auth_header = self.request.headers.get("Authorization")
        if not auth_header or not auth_header.lower().startswith("bearer "):
            return None
        token = auth_header.split()[1]
        try:
            payload = decode_token(token)
        except ValueError:
            return None
        if payload.get("type") != "access":
            return None

        stmt = select(User).where(User.id == int(payload["sub"]))
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def snapshot_session(self, data: dict) -> SessionSnapshot:
        snapshot_id = uuid.uuid4().hex
        expires = settings.security_session_token_ttl_minutes * 60
        key = f"{SNAPSHOT_PREFIX}:{snapshot_id}"
        await self.redis.set(key, json.dumps(data), ex=expires)
        return SessionSnapshot(snapshot_id=snapshot_id, expires_in=expires, payload=data)

    async def consume_snapshot(self, snapshot_id: str) -> dict:
        key = f"{SNAPSHOT_PREFIX}:{snapshot_id}"
        data = await self.redis.get(key)
        if not data:
            return {}
        await self.redis.delete(key)
        return json.loads(data)

    async def _issue_tokens(self, subject: str) -> TokenPair:
        access = create_access_token(subject)
        refresh = create_refresh_token(subject)
        await self.redis.setex(
            f"{REFRESH_TOKEN_PREFIX}:{refresh}",
            settings.refresh_token_expire_minutes * 60,
            refresh,
        )
        return TokenPair(access_token=access, refresh_token=refresh)


async def get_auth_service(
    request: Request,
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
) -> AuthService:
    return AuthService(request=request, session=session, redis=redis)
