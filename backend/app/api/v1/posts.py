from typing import List
from fastapi import APIRouter

router = APIRouter()

@router.get("/posts")
async def list_posts():
    """List all posts"""
    return {"posts": [], "message": "Posts endpoint working"}

@router.get("/posts/{post_id}")
async def get_post(post_id: int):
    """Get a specific post"""
    return {"post_id": post_id, "message": "Get post endpoint working"}

@router.post("/posts")
async def create_post():
    """Create a new post"""
    return {"message": "Create post endpoint working"}
