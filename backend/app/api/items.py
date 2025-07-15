from fastapi import APIRouter, HTTPException, status
from typing import List
from uuid import uuid4
from pydantic import BaseModel, Field

router = APIRouter(prefix="/items", tags=["Items"])

# Простая схема для демо
class Item(BaseModel):
    id: str
    name: str
    description: str | None = None

class ItemCreate(BaseModel):
    name: str
    description: str | None = None

_fake_db: dict[str, Item] = {}

@router.post(
    "/", 
    response_model=Item, 
    status_code=status.HTTP_201_CREATED
)
async def create_item(data: ItemCreate):
    item_id = str(uuid4())
    item = Item(id=item_id, **data.model_dump())
    _fake_db[item_id] = item
    return item

@router.get(
    "/{item_id}", 
    response_model=Item
)
async def read_item(item_id: str):
    item = _fake_db.get(item_id)
    if not item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not found")
    return item

@router.get(
    "/", 
    response_model=List[Item]
)
async def list_items():
    return list(_fake_db.values())
