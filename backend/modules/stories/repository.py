from sqlalchemy.ext.asyncio import AsyncSession

from backend.modules.stories.models import Story


class StoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        title: str,
        content: str,
    ) -> Story:
        story = Story(
            title=title,
            content=content,
        )

        self.db.add(story)
        await self.db.commit()
        await self.db.refresh(story)

        return story