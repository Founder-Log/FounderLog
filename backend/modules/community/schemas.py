from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    content: str = Field(min_length=1)
    tags: list[str] | None = None


class ProjectUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=255)
    content: str | None = Field(default=None, min_length=1)
    tags: list[str] | None = None


class ProjectResponse(BaseModel):
    id: int
    author_id: int
    title: str
    content: str
    status: str
    tags: list[str] | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
