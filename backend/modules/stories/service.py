from sqlalchemy.ext.asyncio import AsyncSession

from backend.modules.stories.repository import StoryRepository
from backend.modules.stories.schemas import StoryCreate


class StoryService:
    def __init__(self, db: AsyncSession):
        self.repository = StoryRepository(db)

    async def create_story(
        self,
        data: StoryCreate,
    ):
        return await self.repository.create(
            title=data.title,
            content=data.content,
        )