from __future__ import annotations

from fastapi import Request
from starlette.datastructures import Headers

from app.schemas.user import TokenRefresh, UserCreatePassword, UserLogin
from app.services.auth import AuthService


def make_request(token: str | None = None) -> Request:
    headers = []
    if token:
        headers.append((b"authorization", f"Bearer {token}".encode()))
    scope = {"type": "http", "headers": headers}
    return Request(scope)


async def test_register_and_login(session, fake_redis):
    service = AuthService(request=make_request(), session=session, redis=fake_redis)

    user = await service.register_password_user(UserCreatePassword(email="user@example.com", password="StrongPass123!"))
    assert user.id is not None

    tokens = await service.authenticate(UserLogin(identifier="user@example.com", password="StrongPass123!"))
    assert tokens.access_token
    assert tokens.refresh_token

    authorized_service = AuthService(request=make_request(tokens.access_token), session=session, redis=fake_redis)
    current = await authorized_service.get_current_user()
    assert current is not None
    assert current.id == user.id

    refreshed = await service.refresh(TokenRefresh(refresh_token=tokens.refresh_token))
    assert refreshed.access_token != tokens.access_token
