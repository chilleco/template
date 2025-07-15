from typing import List, Optional
from beanie import PydanticObjectId
from app.models.user import User

class UserRepository:
    async def create(self, user: User) -> User:
        await user.insert()
        return user

    async def get(self, user_id: str) -> Optional[User]:
        oid = PydanticObjectId(user_id)
        return await User.get(oid)

    async def list(self, skip: int = 0, limit: int = 10) -> List[User]:
        return await User.find_all().skip(skip).limit(limit).to_list()

    async def update(self, user: User, data: dict) -> User:
        data["updated_at"] = datetime.utcnow()
        await user.update({"$set": data})
        return await self.get(str(user.id))

    async def delete(self, user: User) -> None:
        await user.delete()
