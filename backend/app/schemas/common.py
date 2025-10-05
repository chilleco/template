"""Common Pydantic schemas used across the API."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class TimestampedSchema(BaseModel):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
