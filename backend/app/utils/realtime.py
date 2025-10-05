from __future__ import annotations

import json
from typing import Any

from fastapi import WebSocket

from app.models.user import User


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket, user: User | None) -> None:
        await websocket.accept()
        self.active_connections.add(websocket)
        await websocket.send_json({"type": "connection", "status": "connected", "user_id": str(user.id) if user else None})

    async def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.discard(websocket)

    async def handle_message(self, websocket: WebSocket, message: dict[str, Any], user: User | None) -> None:
        event_type = message.get("type")
        if event_type == "ping":
            await websocket.send_json({"type": "pong"})
        else:
            await websocket.send_json({"type": "echo", "payload": message})

    async def broadcast(self, event: str, payload: dict[str, Any]) -> None:
        data = json.dumps({"type": event, "payload": payload})
        for connection in list(self.active_connections):
            await connection.send_text(data)


connection_manager = ConnectionManager()
