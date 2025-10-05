"""Custom typed helpers for configuration readability."""

from __future__ import annotations

from pydantic import PostgresDsn as BasePostgresDsn
from pydantic import RedisDsn as BaseRedisDsn


class PostgresDsn(BasePostgresDsn):
    pass


class RedisDsn(BaseRedisDsn):
    pass
