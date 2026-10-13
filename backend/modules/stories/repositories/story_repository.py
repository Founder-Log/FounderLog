from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.modules.stories.repositories.tag_repository import Tag
from backend.modules.stories.models import Story
from backend.modules.stories.schemas import StoryUpdate, StoryCreate


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