from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.db import get_db
from backend.modules.users.models import User
from backend.core.auth import get_current_user
from backend.modules.stories.schemas import CategoryCreate, CategoryResponse, CategoryUpdate
from backend.modules.stories.services.categories import CategoryService


router = APIRouter(
    prefix="/api/categories",
    tags=["Categories"],
)


@router.get(
    "/",
    response_model=list[CategoryResponse],
    status_code=status.HTTP_200_OK,
)
async def get_categories(
        db: AsyncSession = Depends(get_db)
):
    service = CategoryService(db)

    return await service.get_all_categories()


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
)
async def get_category_by_id(
    category_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = CategoryService(db)

    return await service.get_category_by_id(category_id)


@router.get(
    "/slug/{category_slug}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
)
async def get_category_by_slug(
    category_slug: str,
    db: AsyncSession = Depends(get_db),
):
    service = CategoryService(db)

    return await service.get_category_by_slug(category_slug)


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = CategoryService(db)

    return await service.create_category(data=data, current_user=current_user)


@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
)
async def category_update(
    category_id: int,
    data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = CategoryService(db)

    return await service.category_update(category_id=category_id, data=data, current_user=current_user)


@router.delete(
    "/{category_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def category_delete(
        category_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    service = CategoryService(db)

    await service.category_delete(category_id=category_id, current_user=category_id)
    
    return None