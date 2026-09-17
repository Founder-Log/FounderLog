from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.modules.users.models import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, email: str, handle: str, hashed_password: str) -> User:
        user = User(email=email, handle=handle, hashed_password=hashed_password)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.db.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        return await self.db.scalar(select(User).where(User.email == email))

    async def get_by_handle(self, handle: str) -> User | None:
        return await self.db.scalar(select(User).where(User.handle == handle))
