from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.modules.stories.models import Story, Category, Tag
from backend.modules.stories.schemas import StoryUpdate, StoryCreate, CategoryCreate, CategoryUpdate, TagCreate, TagUpdate


class StoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def create(self, data: StoryCreate) -> Story:
        dump_data=data.model_dump()
        tag_ids=dump_data.pop("tag_ids", [])

        story = Story(**dump_data)

        if tag_ids:
            query = select(Tag).where(Tag.id.in_(tag_ids))
            result = await self.db.execute(query)
            story.tags = list(result.scalars().all())

        self.db.add(story)
        await self.db.commit()
        await self.db.refresh(story)

        return story


    async def update(
            self,
            story: Story, 
            data: StoryUpdate
    ) -> Story:
        update_data = data.model_dump(exclude_unset=True)
        tag_ids = update_data.pop("tag_ids", None)

        for field, value in update_data.items():
            setattr(story, field, value)

        if tag_ids is not None:
            if tag_ids:
                query = select(Tag).where(Tag.id.in_(tag_ids))
                result = await self.db.execute(query)
                story.tags = list(result.scalars().all())
            else:
                story.tags = []

        await self.db.commit()
        await self.db.refresh(story)

        return story


    async def get_all(self) -> Sequence[Story]:
        query = select(Story).where(Story.is_published == True).order_by(Story.id.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()


    async def get_by_id(self, story_id: int, only_published: bool = True) -> Story | None:
        query = select(Story).where(Story.id == story_id)
    
        if only_published:
            query = query.where(Story.is_published == True)

        result = await self.db.execute(query)
        return result.scalar_one_or_none()


    async def delete(self, story: Story) -> None:
        await self.db.delete(story)
        await self.db.commit()


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

class TagRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_tag_by_slug(self, slug: str) -> Tag | None:
        query = select(Tag).where(Tag.slug == slug)
        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def get_tag_by_id(self, tag_id: int) -> Tag | None:
        query = select(Tag).where(Tag.id == tag_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all_tags(self) -> Sequence[Tag]:
        query = select(Tag).order_by(Tag.id.desc())
        result = await self.db.execute(query)

        return result.scalars().all()

    async def create_tag(self, tag_in: TagCreate) -> Tag:
        tag = Tag(**tag_in.model_dump())

        self.db.add(tag)
        await self.db.commit()
        await self.db.refresh(tag)

        return tag

    async def tag_update(self, tag: Tag, data: TagUpdate) -> Tag:
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
                    setattr(tag, field, value)

        await self.db.commit()
        await self.db.refresh(tag)
        return tag 

    async def tag_delete(self, tag: Tag) -> None:
        await self.db.delete(tag)
        await self.db.commit()
