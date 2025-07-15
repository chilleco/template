from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str   # если хешируете пароль в сервисе

class UserUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None

class UserRead(UserBase):
    id: str = Field(..., alias="id")
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "populate_by_name": True,    # читать alias для `id`
        "from_attributes": True,     # брать атрибуты из Document
    }
