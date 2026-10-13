from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from backend.modules.users.models import User
from backend.modules.stories.repository import CategoryRepository
from backend.modules.stories.schemas import CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, db: AsyncSession):
            self.repository = CategoryRepository(db)

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

    async def create_category(self, data: CategoryCreate, current_user: User):

        if not current_user.is_admin:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only administrators can create this category",
                )
        
        category = await self.repository.get_category_by_slug(data.slug)

        if category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this slug already exists",
            )

        return await self.repository.create_category(data)
    

    async def category_update(self, category_id: int, data: CategoryUpdate, current_user: User):

        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only administrators can update this category",
            )
        
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
                    detail="Category with this slug already exists",
                )

        return await self.repository.category_update(category, data)

    async def category_delete(self, category_id: int, current_user: User):

        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only administrators can delete this category",
            )
        
        category = await self.repository.get_category_by_id(category_id)
        return await self.repository.category_delete(category=category)