from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.auth import get_current_user, get_current_user_optional
from backend.core.db import get_db
from backend.modules.community.schemas import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from backend.modules.community.service import (
    NotProjectOwner,
    ProjectNotEditable,
    ProjectNotFound,
    ProjectService,
)

router = APIRouter(prefix="/api/community", tags=["Community"])


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    service = ProjectService(db)
    return await service.create_draft(author_id=user_id, data=data)


@router.get("/", response_model=list[ProjectResponse])
async def list_feed(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
):
    service = ProjectService(db)
    return await service.list_feed(limit=limit, offset=offset)


@router.get("/mine", response_model=list[ProjectResponse])
async def list_my_projects(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user),
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
):
    service = ProjectService(db)
    return await service.list_mine(user_id, limit=limit, offset=offset)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    viewer_id: int | None = Depends(get_current_user_optional),
):
    service = ProjectService(db)
    try:
        return await service.get_visible(project_id, viewer_id)
    except ProjectNotFound:
        raise HTTPException(status_code=404, detail="Пост не найден")


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    data: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    service = ProjectService(db)
    try:
        return await service.update_draft(project_id, user_id, data)
    except ProjectNotFound:
        raise HTTPException(status_code=404, detail="Пост не найден")
    except NotProjectOwner:
        raise HTTPException(status_code=403, detail="Это не ваш пост")
    except ProjectNotEditable:
        raise HTTPException(
            status_code=409, detail="Опубликованный пост нельзя редактировать"
        )


@router.post("/{project_id}/publish", response_model=ProjectResponse)
async def publish_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    service = ProjectService(db)
    try:
        return await service.publish(project_id, user_id)
    except ProjectNotFound:
        raise HTTPException(status_code=404, detail="Пост не найден")
    except NotProjectOwner:
        raise HTTPException(status_code=403, detail="Это не ваш пост")
