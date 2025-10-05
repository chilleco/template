"""Declarative base metadata and model import side effects."""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Ensure models are imported for Alembic autogeneration
from app.models import user  # noqa: F401
from app.models import post  # noqa: F401
