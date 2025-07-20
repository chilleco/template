from fastapi import APIRouter

from .users import router as users_router
from .items import router as items_router

api_v1_router = APIRouter()

# ––– подключаем «ресурс + команды» роуты –––
api_v1_router.include_router(users_router)
api_v1_router.include_router(items_router)

__all__ = ["api_v1_router"]
