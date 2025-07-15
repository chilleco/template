from beanie import Document, Indexed
from pydantic import Field, EmailStr
from datetime import datetime

class User(Document):
    email: EmailStr = Indexed(unique=True)
    name: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
