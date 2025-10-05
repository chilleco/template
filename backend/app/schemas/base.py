from __future__ import annotations

from pydantic import BaseModel


class APIModel(BaseModel):
    model_config = {
        "populate_by_name": True,
        "extra": "forbid",
        "protected_namespaces": (),
        "json_encoders": {},
    }


class PaginationInput(APIModel):
    limit: int = 20
    cursor: str | None = None


class PaginationMeta(APIModel):
    next_cursor: str | None = None
