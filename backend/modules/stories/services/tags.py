from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from backend.modules.users.models import User
from backend.modules.stories.repository import  TagRepository
from backend.modules.stories.schemas import TagCreate, TagUpdate


class TagService:
    def __init__(self, db: AsyncSession):
        self.repository = TagRepository(db)


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
    

    async def create_tag(self, data: TagCreate, current_user: User):

        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can create this tag"
            )
        
        tag = await self.repository.get_tag_by_slug(data.slug)

        if tag:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag with this slug already exists"
            )

        return await self.repository.create_tag(data)
    

    async def tag_update(self, tag_id, data: TagUpdate, current_user: User):

        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="You don't have permission to update this tag"
            )
        
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
    

    async def tag_delete(self, tag_id: int, current_user: User):

        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="You don't have permission to delete this tag"
            )
        
        tag = await self.get_tag_by_id(tag_id)

        return await self.repository.tag_delete(tag=tag)