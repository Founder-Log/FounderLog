from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from backend.modules.stories.schemas.tag import TagResponse
from backend.modules.stories.schemas.category import CategoryResponse
from typing import Optional


class StoryBase(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    origin_url: Optional[str] = None
    is_published: bool = False

    @field_validator("title", "content")
    @classmethod
    def prevent_empty_spaces(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be empty or contain only spaces")
        return v.strip()


class StoryCreate(StoryBase):
    category_id: Optional[int] = None
    tag_ids: list[int] = []


class StoryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    origin_url: Optional[str] = None
    is_published: Optional[bool] = None
    category_id: Optional[int] = None
    tag_ids: Optional[list[int]] = None

    @field_validator("title", "content")
    @classmethod
    def prevent_empty_spaces(cls, v: str | None) -> str | None:
        if v is None:
            return v
        
        if not v.strip():
            raise ValueError("Field cannot be empty or contain only spaces")
            
        return v.strip()


class StoryResponse(StoryBase):
    id: int
    created_at: datetime
    category: Optional[CategoryResponse] = None
    tags: list[TagResponse] = []

    model_config = ConfigDict(from_attributes=True)