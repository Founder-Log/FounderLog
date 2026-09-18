from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.modules.stories.models import Story
from backend.modules.stories.schemas import StoryUpdate


class StoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def create(
        self,
        title: str,
        content: str,
        origin_url: str | None = None,
    ) -> Story:
        story = Story(
            title=title,
            content=content,
            origin_url=origin_url,
        )

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

        for field, value in update_data.items():
            setattr(story, field, value)

        await self.db.commit()
        await self.db.refresh(story)
        return story


    async def get_all(
            self,
    ) -> Sequence[Story]:
        query = select(Story).order_by(Story.id.desc())
        result = await self.db.execute(query)
        return result.scalars().all()


    async def get_by_id(
            self,
            story_id: int
    ) -> Story | None:
        query = select(Story).where(Story.id == story_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


    async def delete(
            self, 
            story: Story
    ) -> None:
        await self.db.delete(story)
        await self.db.commit()