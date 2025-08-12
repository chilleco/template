# from beanie import Document, Indexed
# from pydantic import Field, EmailStr
# from datetime import datetime

# class User(Document):
#     email: EmailStr = Indexed(unique=True)
#     name: str
#     is_active: bool = True
#     created_at: datetime = Field(default_factory=datetime.utcnow)
#     updated_at: datetime = Field(default_factory=datetime.utcnow)

#     class Settings:
#         name = "users"


from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")  # роли: guest, user, moderator, admin, owner
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    posts = relationship("Post", back_populates="author")



class Attachment(Base):
    __tablename__ = "attachments"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    type = Column(String, nullable=False)       # тип вложения: image, file, poll, etc.
    url = Column(String, nullable=False)        # ссылка на хранение (например, URL в Object Storage)
    meta_data = Column(String)                   # renamed from metadata to avoid conflict
    post = relationship("Post", back_populates="attachments")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    author_id = Column(Integer, ForeignKey('users.id'))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
