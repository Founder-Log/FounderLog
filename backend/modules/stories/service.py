from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from backend.modules.stories.repository import StoryRepository
from backend.modules.stories.schemas import StoryCreate, StoryUpdate


class StoryService:
    def __init__(self, db: AsyncSession):
        self.repository = StoryRepository(db)

    async def get_all_stories(self):
        return await self.repository.get_all()

    async def get_story_by_id(
            self,
            story_id: int
    ):
        story = await self.repository.get_by_id(story_id)
        if not story:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The story is not found",
            )
        return story

    async def create_story(
        self,
        data: StoryCreate
    ):
        return await self.repository.create(
            title=data.title,
            content=data.content,
            origin_url=data.origin_url,
        )

    async def story_update(self, story_id: int, data: StoryUpdate):
        story = await self.get_story_by_id(story_id)
        return await self.repository.update(story=story, data=data)


    async def delete_story(
            self,
            story_id: int
    ):
        story = await self.get_story_by_id(story_id)
        return await self.repository.delete(story=story)