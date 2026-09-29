from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.target_type import TargetType
from backend.modules.interactions.models import Comment, Favorite, Vote
from backend.modules.interactions.repository import (
    CommentsRepository,
    FavoritesRepository,
    VotesRepository,
)


class VoteValue(int, Enum):
    UP = 1
    DOWN = -1


class CommentNotFound(Exception):
    pass


class NotCommentOwner(Exception):
    pass


class FavoritesService:
    def __init__(self, db: AsyncSession):
        self.repository = FavoritesRepository(db)

    async def toggle(
        self, user_id: int, target_type: TargetType, target_id: int
    ) -> bool:
        existing = await self.repository.get(user_id, target_type.value, target_id)

        if existing:
            await self.repository.delete(existing)
            return False

        await self.repository.add(
            Favorite(
                user_id=user_id, target_type=target_type.value, target_id=target_id
            )
        )
        return True

    async def list_target_ids(
        self, user_id: int, target_type: TargetType
    ) -> list[int]:
        return await self.repository.list_target_ids(user_id, target_type.value)


class VotesService:
    def __init__(self, db: AsyncSession):
        self.repository = VotesRepository(db)

    async def cast(
        self, user_id: int, target_type: TargetType, target_id: int, value: VoteValue
    ) -> int | None:
        # Повторный клик по той же кнопке снимает голос (toggle),
        # клик по противоположной — перекладывает его, а не плодит вторую запись.
        existing = await self.repository.get(user_id, target_type.value, target_id)

        if existing and existing.value == value.value:
            await self.repository.delete(existing)
            return None

        if existing:
            updated = await self.repository.update_value(existing, value.value)
            return updated.value

        await self.repository.add(
            Vote(
                user_id=user_id,
                target_type=target_type.value,
                target_id=target_id,
                value=value.value,
            )
        )
        return value.value

    async def get_score(self, target_type: TargetType, target_id: int) -> int:
        return await self.repository.get_score(target_type.value, target_id)


class CommentsService:
    def __init__(self, db: AsyncSession):
        self.repository = CommentsRepository(db)

    async def create(
        self,
        user_id: int,
        target_type: TargetType,
        target_id: int,
        content: str,
        parent_id: int | None = None,
    ) -> Comment:
        return await self.repository.add(
            Comment(
                user_id=user_id,
                target_type=target_type.value,
                target_id=target_id,
                content=content,
                parent_id=parent_id,
            )
        )

    async def get_thread(self, target_type: TargetType, target_id: int) -> list[Comment]:
        return await self.repository.get_thread(target_type.value, target_id)

    async def delete(self, comment_id: int, user_id: int) -> None:
        comment = await self.repository.get(comment_id)
        if comment is None:
            raise CommentNotFound(comment_id)
        if comment.user_id != user_id:
            raise NotCommentOwner(comment_id)

        await self.repository.delete(comment)