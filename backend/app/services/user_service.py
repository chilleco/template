from typing import List
from datetime import datetime
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.user_repo import UserRepository
from loguru import logger

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    async def create_user(self, data: UserCreate) -> dict:
        # Здесь можно захешировать пароль, отправить welcome email и т.д.
        user = User(**data.model_dump(exclude={"password"}))
        created = await self.repo.create(user)
        logger.info("user.created", user_id=str(created.id), email=created.email)
        # Convert User object to dict with string ID for proper serialization
        user_dict = created.model_dump()
        user_dict["id"] = str(created.id)  # Convert ObjectId to string directly from Document
        return user_dict

    async def get_user(self, user_id: str) -> dict | None:
        user = await self.repo.get(user_id)
        if not user:
            return None
        # Convert User object to dict with string ID for proper serialization
        user_dict = user.model_dump()
        user_dict["id"] = str(user.id)  # Convert ObjectId to string directly from Document
        return user_dict

    async def list_users(self, skip: int = 0, limit: int = 10) -> List[dict]:
        users = await self.repo.list(skip, limit)
        # Convert User objects to dicts with string IDs for proper serialization
        result = []
        for user in users:
            user_dict = user.model_dump()
            user_dict["id"] = str(user.id)  # Convert ObjectId to string directly from Document
            result.append(user_dict)
        return result

    async def update_user(self, user_id: str, data: UserUpdate) -> User:
        user = await self.repo.get(user_id)
        if not user:
            raise ValueError("User not found")
        update_data = data.model_dump(exclude_unset=True)
        updated = await self.repo.update(user, update_data)
        logger.info("user.updated", user_id=user_id)
        return updated

    async def delete_user(self, user_id: str) -> None:
        user = await self.repo.get(user_id)
        if not user:
            raise ValueError("User not found")
        await self.repo.delete(user)
        logger.info("user.deleted", user_id=user_id)
