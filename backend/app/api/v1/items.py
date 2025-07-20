from typing import List
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(tags=["Items"])

# ––– очень упрощённая in-memory реализация (пример RPC-эндпойнтов) ––– #
class Item(BaseModel):
    id: str
    name: str
    description: str | None = None

class ItemCreate(BaseModel):
    name: str
    description: str | None = None


_FAKE_DB: dict[str, Item] = {}


@router.post(
    "/items",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    summary="Create item (RPC POST)",
)
async def create_item(data: ItemCreate):
    item_id = str(uuid4())
    item = Item(id=item_id, **data.model_dump())
    _FAKE_DB[item_id] = item
    return item


@router.get(
    "/items/{item_id}",
    response_model=Item,
    summary="Retrieve item",
)
async def retrieve_item(item_id: str):
    if item_id not in _FAKE_DB:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not found")
    return _FAKE_DB[item_id]


@router.get(
    "/items",
    response_model=List[Item],
    summary="List items",
)
async def list_items():
    return list(_FAKE_DB.values())


@router.post(
    "/items/{item_id}/archive",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Archive item (command via POST)",
)
async def archive_item(item_id: str):
    if item_id not in _FAKE_DB:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not found")
    _FAKE_DB[item_id].description = "ARCHIVED"
