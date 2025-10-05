from __future__ import annotations

import secrets
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_pre_auth_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.core.settings import settings
from app.models.user import Role, RolePermission, User, UserRole, UserSession
from app.schemas.user import AuthResponse, PreAuthState, SessionState, TokenPair, UserRead
from app.services.access import AccessService, DEFAULT_PERMISSIONS


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def bootstrap_default_roles(self) -> None:
        result = await self.session.execute(select(Role))
        if result.first():
            return
        admin_role = Role(name="Administrator", slug="admin")
        editor_role = Role(name="Editor", slug="editor")
        viewer_role = Role(name="Viewer", slug="viewer")
        self.session.add_all([admin_role, editor_role, viewer_role])
        await self.session.flush()

        def assign(role: Role, permissions: set[str]) -> None:
            for perm in permissions:
                self.session.add(RolePermission(role_id=role.id, permission=perm))

        assign(admin_role, DEFAULT_PERMISSIONS)
        assign(
            editor_role,
            {
                "post:create",
                "post:update",
                "post:publish",
                "analytics:view",
            },
        )
        assign(viewer_role, {"post:read"})

    async def ensure_pre_auth_session(self, token: str | None, data: dict | None = None) -> PreAuthState:
        now = datetime.now(timezone.utc)
        if token:
            query = select(UserSession).where(UserSession.pre_auth_token == token)
            existing = (await self.session.execute(query)).scalar_one_or_none()
            if existing and existing.expires_at > now:
                if data:
                    existing.data.update(data)
                    await self.session.flush()
                return PreAuthState(token=existing.pre_auth_token, expires_at=existing.expires_at, data=existing.data)

        pre_auth_token = create_pre_auth_token(secrets.token_urlsafe(32))
        expires_at = now + timedelta(minutes=settings.pre_auth_token_expire_minutes)
        session = UserSession(pre_auth_token=pre_auth_token, data=data or {}, expires_at=expires_at)
        self.session.add(session)
        await self.session.flush()
        return PreAuthState(token=pre_auth_token, expires_at=expires_at, data=session.data)

    async def register_local_user(self, *, email: str, password: str, full_name: str | None, session_token: str) -> AuthResponse:
        existing = await self._get_user_by_email(email)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email_already_registered")

        user = User(email=email, hashed_password=hash_password(password), full_name=full_name, is_active=True)
        self.session.add(user)
        await self.session.flush()

        await self._attach_session_to_user(session_token=session_token, user=user)
        return await self._issue_auth_bundle(user, session_token)

    async def authenticate_local(self, *, email: str, password: str, session_token: str) -> AuthResponse:
        user = await self._get_user_by_email(email)
        if not user or not user.hashed_password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_credentials")
        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_credentials")
        await self._assert_user_allowed(user)
        await self._attach_session_to_user(session_token=session_token, user=user)
        return await self._issue_auth_bundle(user, session_token)

    async def rotate_tokens(self, refresh_token: str) -> TokenPair:
        payload = self._decode(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_token")
        user = await self.session.get(User, uuid.UUID(payload["sub"]))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user_not_found")
        await self._assert_user_allowed(user)
        return TokenPair(access_token=create_access_token(str(user.id)), refresh_token=create_refresh_token(str(user.id)))

    async def _issue_auth_bundle(self, user: User, session_token: str) -> AuthResponse:
        tokens = TokenPair(
            access_token=create_access_token(str(user.id)),
            refresh_token=create_refresh_token(str(user.id)),
        )
        session_state = await self.ensure_pre_auth_session(session_token)
        user_read = await self._user_to_schema(user)
        return AuthResponse(user=user_read, tokens=tokens, session=SessionState(**session_state.model_dump()))

    async def _attach_session_to_user(self, *, session_token: str, user: User) -> None:
        query = select(UserSession).where(UserSession.pre_auth_token == session_token)
        session = (await self.session.execute(query)).scalar_one_or_none()
        if session:
            session.user_id = user.id
            await self.session.flush()
            return

        expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.pre_auth_token_expire_minutes)
        session = UserSession(pre_auth_token=session_token, user_id=user.id, data={}, expires_at=expires_at)
        self.session.add(session)
        await self.session.flush()

    async def _user_to_schema(self, user: User) -> UserRead:
        permissions = sorted(AccessService(user).user_permissions())
        roles = [role.slug for role in user.roles]
        return UserRead(
            id=user.id,
            email=user.email,
            phone_e164=user.phone_e164,
            username=user.username,
            full_name=user.full_name,
            locale=user.locale,
            timezone=user.timezone,
            is_active=user.is_active,
            is_verified=user.is_verified,
            is_superuser=user.is_superuser,
            banned_until=user.banned_until,
            roles=roles,
            permissions=permissions,
        )

    async def _get_user_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    def _decode(self, token: str) -> dict | None:
        from app.core.security import decode_token

        return decode_token(token)

    async def _assert_user_allowed(self, user: User) -> None:
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user_inactive")
        if user.banned_until and user.banned_until > datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user_banned")
