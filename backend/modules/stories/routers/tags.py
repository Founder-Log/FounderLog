from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.db import get_db
from backend.core.auth import get_current_user
from backend.modules.stories.schemas import TagCreate, TagResponse, TagUpdate
from backend.modules.stories.service import TagService


router = APIRouter(
    prefix="/api/tags",
    tags=["Tags"],
)


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