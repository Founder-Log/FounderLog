from pydantic import BaseModel, ConfigDict
from typing import Optional


class StoryBase(BaseModel):
    title: str
    content: str
    origin_url: Optional[str] = None
    is_published: bool = False


class StoryCreate(StoryBase):
    pass


class StoryResponse(StoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class StoryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    origin_url: Optional[str] = None
    is_published: Optional[bool] = None