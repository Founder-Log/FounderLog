from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from backend.modules.interactions.models import Comment, Favorite, Vote


class FavoritesRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(
        self, user_id: int, target_type: str, target_id: int
    ) -> Favorite | None:
        return await self.db.scalar(
            select(Favorite).where(
                Favorite.user_id == user_id,
                Favorite.target_type == target_type,
                Favorite.target_id == target_id,
            )
        )

    async def add(self, favorite: Favorite) -> Favorite:
        self.db.add(favorite)
        await self.db.commit()
        return favorite

    async def delete(self, favorite: Favorite) -> None:
        await self.db.delete(favorite)
        await self.db.commit()

    async def list_target_ids(self, user_id: int, target_type: str) -> list[int]:
        result = await self.db.execute(
            select(Favorite.target_id).where(
                Favorite.user_id == user_id,
                Favorite.target_type == target_type,
            )
        )
        return [row[0] for row in result.all()]


class VotesRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, user_id: int, target_type: str, target_id: int) -> Vote | None:
        return await self.db.scalar(
            select(Vote).where(
                Vote.user_id == user_id,
                Vote.target_type == target_type,
                Vote.target_id == target_id,
            )
        )

    async def add(self, vote: Vote) -> Vote:
        self.db.add(vote)
        await self.db.commit()
        await self.db.refresh(vote)
        return vote

    async def update_value(self, vote: Vote, value: int) -> Vote:
        vote.value = value
        await self.db.commit()
        await self.db.refresh(vote)
        return vote

    async def delete(self, vote: Vote) -> None:
        await self.db.delete(vote)
        await self.db.commit()

    async def get_score(self, target_type: str, target_id: int) -> int:
        result = await self.db.scalar(
            select(func.coalesce(func.sum(Vote.value), 0)).where(
                Vote.target_type == target_type,
                Vote.target_id == target_id,
            )
        )
        return int(result)


class CommentsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, comment: Comment) -> Comment:
        self.db.add(comment)
        await self.db.commit()
        await self.db.refresh(comment)
        return comment

    async def get(self, comment_id: int) -> Comment | None:
        return await self.db.get(Comment, comment_id)

    async def delete(self, comment: Comment) -> None:
        await self.db.delete(comment)
        await self.db.commit()

    async def get_thread(self, target_type: str, target_id: int) -> list[Comment]:
        base_query = select(Comment).where(
            Comment.target_type == target_type,
            Comment.target_id == target_id,
            Comment.parent_id.is_(None),
        )
        cte = base_query.cte(name="comment_tree", recursive=True)
        cte_alias = aliased(Comment, cte)

        recursive_query = select(Comment).join(
            cte_alias, Comment.parent_id == cte_alias.id
        )
        cte = cte.union_all(recursive_query)

        tree_alias = aliased(Comment, cte)
        result = await self.db.execute(
            select(tree_alias).order_by(tree_alias.created_at)
        )
        return list(result.scalars().all())