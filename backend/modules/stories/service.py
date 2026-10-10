from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from backend.modules.stories.repository import StoryRepository, CategoryRepository, TagRepository
from backend.modules.stories.schemas import StoryCreate, StoryUpdate, CategoryCreate, CategoryUpdate, TagCreate, TagUpdate


class StoryService:
    def __init__(self, db: AsyncSession):
        self.repository = StoryRepository(db)

    async def get_all_stories(self):
        return await self.repository.get_all()

    async def get_story_by_id(
            self,
            story_id: int,
            only_published: bool = True
    ):
        story = await self.repository.get_by_id(story_id, only_published=only_published)
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
        story = await self.get_story_by_id(story_id, only_published=False)
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
        story = await self.get_story_by_id(story_id, only_published=False)
        return await self.repository.delete(story=story)


class CategoryService:
    def __init__(self, repository: CategoryRepository):
            self.repository = repository

    async def get_all_categories(self):
        return await self.repository.get_all_categories()

    async def get_category_by_slug(self, slug:str):
        category = await self.repository.get_category_by_slug(slug)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The category is not found",
            )

        return category

    async def get_category_by_id(self, category_id: int):
        category = await self.repository.get_category_by_id(category_id)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The category is not found",
            )

        return category

    async def create_category(self, data: CategoryCreate):
        category = await self.repository.get_category_by_slug(data.slug)
        if category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this slug already exists",
            )

        return await self.repository.create_category(data)

    async def category_update(self, category_id: int, data: CategoryUpdate):
        category = await self.repository.get_category_by_id(category_id)

        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided for update"
            )

        if data.slug and data.slug != category.slug:
            existing_tag = await self.repository.get_tag_by_slug(data.slug)
            if existing_tag:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Tag with this slug already exists",
                )

        return await self.repository.category_update(category, data)

    async def category_delete(self, category_id: int):
        category = await self.repository.get_category_by_id(category_id)
        return await self.repository.category_delete(category=category)


class TagService:
    def __init__(self, repository: TagRepository):
        self.repository = repository

    async def get_all_tags(self):
        return await self.repository.get_all_tags()

    async def get_tag_by_slug(self, slug: str):
        tag = await self.repository.get_tag_by_slug(slug)

        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The tag is not found",
            )

        return tag

    async def get_tag_by_id(self, tag_id: int):
        tag = await self.repository.get_tag_by_id(tag_id)

        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The tag is not found",
            )

        return tag

    async def create_tag(self, data: TagCreate):
        tag = await self.repository.get_tag_by_slug(data.slug)

        if tag:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag with this slug already exists"
            )

        return await self.repository.create_tag(data)

    async def tag_update(self, tag_id, data: TagUpdate):
        tag = await self.get_tag_by_id(tag_id)

        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided for update",
            )

        if data.slug and data.slug != tag.slug:
            existing_tag = await self.repository.get_tag_by_slug(data.slug)
            if existing_tag:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Tag with this slug already exists",
                )

        return await self.repository.tag_update(tag, data)

    async def tag_delete(self, tag_id: int):
        tag = await self.get_tag_by_id(tag_id)
        return await self.repository.tag_delete(tag=tag)