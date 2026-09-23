from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


class TagBase(BaseModel):
    name: str
    slug: str


class TagCreate(TagBase):
    pass


class TagResponse(TagBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CategoryBase(BaseModel):
    name: str
    slug: str


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class StoryBase(BaseModel):
    title: str
    content: str
    origin_url: Optional[str] = None
    is_published: bool = False


class StoryCreate(StoryBase):
    category_id: Optional[int] = None
    tag_ids: list[int] = []


class StoryResponse(StoryBase):
    id: int
    created_at: datetime
    category: Optional[CategoryResponse] = None
    tags: list[TagResponse] = []

    model_config = ConfigDict(from_attributes=True)


class StoryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    origin_url: Optional[str] = None
    is_published: Optional[bool] = None