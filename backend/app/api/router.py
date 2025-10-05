"""Aggregate API routers and shared dependencies."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.v1 import routes as v1_routes


api_router = APIRouter(prefix="/api")
api_router.include_router(v1_routes.router, prefix="/v1")

__all__ = ["api_router"]
