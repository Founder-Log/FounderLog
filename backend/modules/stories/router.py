from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.db import get_db
from backend.modules.stories.schemas import StoryCreate, StoryResponse
from backend.modules.stories.service import StoryService


router = APIRouter(
    prefix="/api/stories",
    tags=["Stories"],
)


@router.post(
    "/",
    response_model=StoryResponse,
)
async def create_story(
    data: StoryCreate,
    db: AsyncSession = Depends(get_db),
):
    service = StoryService(db)

    return await service.create_story(data)