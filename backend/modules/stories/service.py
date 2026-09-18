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
        if not data.title.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title cannot be empty",
            )

        if not data.content.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Content cannot be empty",
            )
        
        return await self.repository.create(
            title=data.title,
            content=data.content,
            origin_url=data.origin_url,
        )

    async def story_update(self, story_id: int, data: StoryUpdate):
        story = await self.get_story_by_id(story_id)
        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided for update",
            )

        if "title" in update_data:
            if update_data["title"] is None or not update_data["title"].strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Title cannot be empty",
                )

        if "content" in update_data:
            if update_data["content"] is None or not update_data["content"].strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Content cannot be empty",
                )
        return await self.repository.update(story=story, data=data)


    async def delete_story(
            self,
            story_id: int
    ):
        story = await self.get_story_by_id(story_id)
        return await self.repository.delete(story=story)