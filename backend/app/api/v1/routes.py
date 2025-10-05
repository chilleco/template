"""Versioned API router assembly."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.v1 import dependencies
from app.api.v1.routes import auth, posts, users, websocket

router = APIRouter()

router.include_router(auth.router, tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(posts.router, prefix="/posts", tags=["posts"])
router.include_router(websocket.router, prefix="/ws", tags=["ws"])

__all__ = ["router"]
