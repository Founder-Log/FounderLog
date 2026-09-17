from pydantic import BaseModel, ConfigDict
from typing import Optional


class StoryBase(BaseModel):
    title: str
    content: str
    source_url: Optional[str] = None


class StoryCreate(StoryBase):
    pass


class StoryResponse(StoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class StoryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    source_url: Optional[str] = None
