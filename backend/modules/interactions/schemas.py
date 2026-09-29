from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class VoteRequest(BaseModel):
    target_type: str
    target_id: int
    value: Literal[1, -1]


class VoteResponse(BaseModel):
    value: int | None
    score: int


class ScoreResponse(BaseModel):
    score: int


class CommentCreate(BaseModel):
    target_type: str
    target_id: int
    content: str = Field(min_length=1, max_length=4000)
    parent_id: int | None = None


class CommentResponse(BaseModel):
    id: int
    user_id: int
    target_type: str
    target_id: int
    parent_id: int | None
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)