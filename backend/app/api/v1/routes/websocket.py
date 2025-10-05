"""Realtime websocket endpoints."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

_connected_clients: set[WebSocket] = set()


@router.websocket("/notifications")
async def websocket_notifications(websocket: WebSocket):
    await websocket.accept()
    _connected_clients.add(websocket)
    try:
        while True:
            message: dict[str, Any] = await websocket.receive_json()
            await broadcast(message)
    except WebSocketDisconnect:
        _connected_clients.remove(websocket)


async def broadcast(message: dict[str, Any]) -> None:
    for client in list(_connected_clients):
        await client.send_json(message)
