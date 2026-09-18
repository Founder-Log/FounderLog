from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.db import get_db
from backend.core.auth import get_current_user
from backend.modules.stories.schemas import StoryCreate, StoryResponse, StoryUpdate
from backend.modules.stories.service import StoryService


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