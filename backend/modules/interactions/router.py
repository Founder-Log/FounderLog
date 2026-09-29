from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.auth import get_current_user
from backend.core.db import get_db
from backend.core.target_type import TargetType
from backend.modules.interactions.schemas import (
    CommentCreate,
    CommentResponse,
    ScoreResponse,
    VoteRequest,
    VoteResponse,
)
from backend.modules.interactions.service import (
    CommentNotFound,
    CommentsService,
    NotCommentOwner,
    VotesService,
    VoteValue,
)

router = APIRouter(prefix="/api", tags=["Interactions"])


def _parse_target_type(value: str) -> TargetType:
    try:
        return TargetType(value)
    except ValueError:
        raise HTTPException(status_code=400, detail="Неизвестный target_type")


@router.post("/votes", response_model=VoteResponse)
async def cast_vote(
    data: VoteRequest,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    target_type = _parse_target_type(data.target_type)
    service = VotesService(db)
    current = await service.cast(
        user_id, target_type, data.target_id, VoteValue(data.value)
    )
    score = await service.get_score(target_type, data.target_id)
    return VoteResponse(value=current, score=score)


@router.get("/votes", response_model=ScoreResponse)
async def get_votes(
    target_type: str,
    target_id: int,
    db: AsyncSession = Depends(get_db),
):
    parsed = _parse_target_type(target_type)
    service = VotesService(db)
    return ScoreResponse(score=await service.get_score(parsed, target_id))


@router.post(
    "/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    target_type = _parse_target_type(data.target_type)
    service = CommentsService(db)
    return await service.create(
        user_id=user_id,
        target_type=target_type,
        target_id=data.target_id,
        content=data.content,
        parent_id=data.parent_id,
    )


@router.get("/comments", response_model=list[CommentResponse])
async def get_comments(
    target_type: str,
    target_id: int,
    db: AsyncSession = Depends(get_db),
):
    parsed = _parse_target_type(target_type)
    service = CommentsService(db)
    return await service.get_thread(parsed, target_id)


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    service = CommentsService(db)
    try:
        await service.delete(comment_id, user_id)
    except CommentNotFound:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    except NotCommentOwner:
        raise HTTPException(status_code=403, detail="Это не ваш комментарий")