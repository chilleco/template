from __future__ import annotations

import pytest

from app.services.auth import AuthService

pytestmark = pytest.mark.asyncio


async def test_register_and_login_flow(db_session):
    service = AuthService(db_session)
    await service.bootstrap_default_roles()
    session_state = await service.ensure_pre_auth_session(None)

    registered = await service.register_local_user(
        email="user@example.com",
        password="secret123",
        full_name="Example User",
        session_token=session_state.token,
    )

    assert registered.user.email == "user@example.com"
    await db_session.commit()

    login_session = await service.ensure_pre_auth_session(registered.session.token)
    logged_in = await service.authenticate_local(
        email="user@example.com",
        password="secret123",
        session_token=login_session.token,
    )

    assert logged_in.tokens.access_token
    assert logged_in.user.email == "user@example.com"
