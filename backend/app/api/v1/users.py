from typing import List

from fastapi import APIRouter, HTTPException, status
from myapp.schemas.user import UserCreate, UserRead, UserUpdate
from myapp.services.user_service import UserService

router = APIRouter(tags=["Users"])
_svc = UserService()                     # можно заменить на Depends(UserService)

# ---------------------------------------------------------------- #
#  OpenAI / Stripe style:                                          #
#   • POST /v1/users              -> create                        #
#   • GET  /v1/users/{id}         -> retrieve                      #
#   • GET  /v1/users              -> list                          #
#   • POST /v1/users/{id}/deactivate  -> «команда» над ресурсом    #
#   • POST /v1/users/{id}/update      -> частичное обновление      #
# ---------------------------------------------------------------- #

@router.post(
    "/users",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create user (RPC POST)",
)
async def create_user(payload: UserCreate):
    return await _svc.create_user(payload)


@router.get(
    "/users/{user_id}",
    response_model=UserRead,
    summary="Get user by ID",
)
async def retrieve_user(user_id: str):
    user = await _svc.get_user(user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return user


@router.get(
    "/users",
    response_model=List[UserRead],
    summary="List users (GET for cache-friendliness)",
)
async def list_users(skip: int = 0, limit: int = 10):
    return await _svc.list_users(skip, limit)


@router.post(
    "/users/{user_id}/update",
    response_model=UserRead,
    summary="Partial update (RPC POST)",
)
async def update_user(user_id: str, payload: UserUpdate):
    try:
        return await _svc.update_user(user_id, payload)
    except ValueError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")


@router.post(
    "/users/{user_id}/deactivate",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deactivate account (command pattern)",
)
async def deactivate_user(user_id: str):
    try:
        await _svc.update_user(user_id, UserUpdate(is_active=False))
    except ValueError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
