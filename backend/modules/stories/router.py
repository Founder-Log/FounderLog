from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.db import get_db
from backend.core.auth import get_current_user
from backend.modules.stories.schemas import StoryCreate, StoryResponse, StoryUpdate,CategoryCreate, CategoryResponse, CategoryUpdate, TagCreate, TagResponse, TagUpdate
from backend.modules.stories.service import StoryService, CategoryService, TagService


router = APIRouter(
    prefix="/api/stories",
    tags=["Stories"],
)


@router.get(
    "/",
    response_model=list[StoryResponse],
    status_code=status.HTTP_200_OK,
)
async def get_stories(
    db: AsyncSession = Depends(get_db),
):
    service = StoryService(db)
    
    return await service.get_all_stories()


@router.get(
        "/{story_id}",
        response_model=StoryResponse,
        status_code=status.HTTP_200_OK,
)
async def get_story(
    story_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = StoryService(db)
    return await service.get_story_by_id(story_id)


@router.post(
    "/",
    response_model=StoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_story(
    data: StoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = StoryService(db)

    return await service.create_story(data)


@router.patch(
    "/{story_id}",
    response_model=StoryResponse,
    status_code=status.HTTP_200_OK,
)
async def story_update(
    story_id: int,
    data: StoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = StoryService(db)

    return await service.story_update(story_id=story_id, data=data)


@router.delete(
    "/{story_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def story_delete(
    story_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    service = StoryService(db)
    await service.delete_story(story_id)
    return None


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
    current_user: dict = Depends(get_current_user)
):
    service = CategoryService(db)

    return await service.create_category(data)


@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
)
async def category_update(
    category_id: int,
    data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    service = CategoryService(db)

    return await service.category_update(category_id=category_id, data=data)


@router.delete(
    "/{category_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def category_delete(
        category_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    service = CategoryService(db)

    await service.category_delete(category_id)
    return None


@router.get(
    "/",
    response_model=list[TagResponse],
    status_code=status.HTTP_200_OK,
)
async def get_tags(
    db: AsyncSession = Depends(get_db)
):
    service = TagService(db)

    return await service.get_all_tags()


@router.get(
    "/{tag_id}",
    response_model=TagResponse,
    status_code=status.HTTP_200_OK,
)
async def get_tag_by_id(
    tag_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = TagService(db)

    return await service.get_tag_by_id(tag_id=tag_id)


@router.get(
        "/slug/{tag_slug}",
        response_model=TagResponse,
        status_code=status.HTTP_200_OK,
)
async def get_tag_by_slug(
    tag_slug: str,
    db: AsyncSession = Depends(get_db),
):
    service = TagService(db)

    return await service.get_tag_by_slug(tag_slug=tag_slug)


@router.post(
    "/",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_tag(
    data: TagCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = TagService(db)

    return await service.create_tag(data=data)


@router.patch(
    "/{tag_id}",
    response_model=TagResponse,
    status_code=status.HTTP_200_OK,
)
async def tag_update(
    tag_id: int,
    data: TagUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    service = TagService(db)

    return await service.tag_update(tag_id=tag_id, data=data)


@router.delete(
    "/{tag_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def tag_delete(
    tag_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = TagService(db)

    await service.tag_delete(tag_id=tag_id)
    return None
    