from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_session
from ..models.post import Post
from ..schemas.post import PostCreate, PostRead

router = APIRouter()

@router.get("/", response_model=List[PostRead])
async def list_posts(db: AsyncSession = Depends(get_session), page: int = 1, page_size: int = 20):
    # Query posts from the database (possibly from a read replica)
    result = await db.execute(
        select(Post).order_by(Post.created_at.desc()).limit(page_size).offset((page-1)*page_size)
    )
    posts = result.scalars().all()
    return posts

@router.get("/{post_id}", response_model=PostRead)
async def get_post(post_id: int, db: AsyncSession = Depends(get_session)):
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("/", response_model=PostRead)
async def create_post(new_post: PostCreate, db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    # Only authenticated users (depends get_current_user) can create
    post = Post(title=new_post.title, content=new_post.content, author_id=current_user.id)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    # Optionally notify via WebSocket or background task
    logger.info(f"User {current_user.id} created post {post.id}")
    return post
