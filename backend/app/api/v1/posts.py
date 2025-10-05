from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session, get_optional_user, require_permission
from app.models.user import User
from app.schemas.base import PaginationInput
from app.schemas.post import PostCreate, PostListResponse, PostRead, PostUpdate
from app.services.posts import PostService

router = APIRouter()


@router.post("/list", response_model=PostListResponse)
async def list_posts(
    payload: PaginationInput,
    session: AsyncSession = Depends(get_db_session),
    current_user: User | None = Depends(get_optional_user),
) -> dict:
    service = PostService(session, actor=current_user)
    posts, meta = await service.list_posts(payload, include_unpublished=bool(current_user))
    return PostListResponse(items=posts, meta=meta)


@router.post("/detail", response_model=PostRead)
async def get_post(
    payload: dict,
    session: AsyncSession = Depends(get_db_session),
    current_user: User | None = Depends(get_optional_user),
) -> PostRead:
    slug = payload.get("slug")
    if not slug:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="missing_slug")
    service = PostService(session, actor=current_user)
    return await service.get_post(slug)


@router.post("/create", response_model=PostRead)
async def create_post(
    payload: PostCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(require_permission("post:create")),
) -> PostRead:
    service = PostService(session, actor=current_user)
    return await service.create_post(payload)


@router.post("/update", response_model=PostRead)
async def update_post(
    payload: PostUpdate,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(require_permission("post:update")),
) -> PostRead:
    service = PostService(session, actor=current_user)
    return await service.update_post(payload)
