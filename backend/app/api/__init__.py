"""Expose combined routers to main app."""

from fastapi import APIRouter

from app.api.v1.endpoints import users, items  # ← примеры

api_router = APIRouter()
api_router.include_router(users.router, tags=["Users"])
api_router.include_router(items.router, tags=["Items"])
