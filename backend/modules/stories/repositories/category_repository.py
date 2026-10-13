from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.modules.stories.models import Category
from backend.modules.stories.schemas import CategoryCreate, CategoryUpdate


class CategoryRepository:
    def __init__(self, db: AsyncSession):
            self.db = db

    async def get_category_by_slug(self, slug: str) -> Category | None:
        query = select(Category).where(Category.slug == slug)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_category_by_id(self, category_id: int) -> Category | None:
        query = select(Category).where(Category.id == category_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all_categories(self) -> Sequence[Category]:
        query = select(Category).order_by(Category.id.desc())
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_category(self, category_in: CategoryCreate) -> Category:
        category = Category(**category_in.model_dump())

        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        
        return category

    async def category_update(self, category: Category, data: CategoryUpdate) -> Category:
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
                    setattr(category, field, value)

        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def category_delete(self, category: Category) -> None:
        await self.db.delete(category)
        await self.db.commit()