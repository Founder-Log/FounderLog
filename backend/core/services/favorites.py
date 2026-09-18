from enum import Enum

from sqlalchemy import Integer, String, UniqueConstraint, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.db import Base


class TargetType(str, Enum):
    STORY = "story"
    PROJECT = "project"


class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (
        UniqueConstraint(
            "user_id", "target_type", "target_id", name="uq_favorite_per_user_target"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    target_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    target_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)


class FavoritesService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def toggle(
        self, user_id: int, target_type: TargetType, target_id: int
    ) -> bool:
        existing = await self.db.scalar(
            select(Favorite).where(
                Favorite.user_id == user_id,
                Favorite.target_type == target_type.value,
                Favorite.target_id == target_id,
            )
        )

        if existing:
            await self.db.delete(existing)
            await self.db.commit()
            return False

        self.db.add(
            Favorite(
                user_id=user_id, target_type=target_type.value, target_id=target_id
            )
        )
        await self.db.commit()
        return True

    async def list_target_ids(
        self, user_id: int, target_type: TargetType
    ) -> list[int]:
        result = await self.db.execute(
            select(Favorite.target_id).where(
                Favorite.user_id == user_id,
                Favorite.target_type == target_type.value,
            )
        )
        return [row[0] for row in result.all()]
