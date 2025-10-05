from __future__ import annotations

import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.security import decode_token, TokenSubject
from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.utils.realtime import connection_manager

router = APIRouter()


async def _user_from_token(token: str | None) -> User | None:
    if not token:
        return None
    payload = decode_token(token)
    if not payload or payload.get("type") != TokenSubject.ACCESS:
        return None
    try:
        user_id = uuid.UUID(payload["sub"])
    except (KeyError, ValueError):
        return None
    async with AsyncSessionLocal() as session:
        return await session.get(User, user_id)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    token = websocket.query_params.get("token")
    user = await _user_from_token(token)
    await connection_manager.connect(websocket, user)
    try:
        while True:
            message = await websocket.receive_json()
            await connection_manager.handle_message(websocket, message, user)
    except WebSocketDisconnect:
        await connection_manager.disconnect(websocket)
