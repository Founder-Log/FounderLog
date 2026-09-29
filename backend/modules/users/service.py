from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.auth import create_access_token
from backend.modules.users.models import User
from backend.modules.users.repository import UserRepository
from backend.modules.users.schemas import UserRegister

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class EmailAlreadyRegistered(Exception):
    pass


class HandleAlreadyTaken(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class UserNotFound(Exception):
    pass


class UserService:
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def register(self, data: UserRegister) -> User:
        if await self.repository.get_by_email(data.email):
            raise EmailAlreadyRegistered(data.email)
        if await self.repository.get_by_handle(data.handle):
            raise HandleAlreadyTaken(data.handle)

        hashed = pwd_context.hash(data.password)
        return await self.repository.create(
            email=data.email, handle=data.handle, hashed_password=hashed
        )

    async def authenticate(self, email: str, password: str) -> str:
        user = await self.repository.get_by_email(email)
        if user is None or not pwd_context.verify(password, user.hashed_password):
            raise InvalidCredentials()

        return create_access_token(user.id, is_admin=user.is_admin)

    async def get_profile(self, user_id: int) -> User:
        user = await self.repository.get_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)
        return user
