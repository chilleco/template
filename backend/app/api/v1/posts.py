from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.post import PostCreate, PostRead, PostUpdate
from app.services.post_service import PostService

router = APIRouter()
_svc = PostService()

@router.get("/posts", response_model=List[PostRead])
async def list_posts(skip: int = 0, limit: int = 10):
    """List all posts"""
    return await _svc.list_posts(skip=skip, limit=limit)

@router.get("/posts/{post_id}", response_model=PostRead)
async def get_post(post_id: int):
    """Get a specific post"""
    post = await _svc.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("/posts", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(data: PostCreate):
    """Create a new post"""
    # For now, using a dummy author_id of 1 since we don't have authentication
    return await _svc.create_post(data, author_id=1)
