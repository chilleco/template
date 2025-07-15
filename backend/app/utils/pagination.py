from fastapi import Query
from typing import Tuple

def pagination_params(
    default_limit: int = 10, 
    max_limit: int = 100
) -> Tuple[int, int]:
    """
    Returns (skip, limit) from query params:
      ?skip=0&limit=10
    """
    skip: int = Query(0, ge=0)
    limit: int = Query(default_limit, ge=1, le=max_limit)
    return skip, limit
