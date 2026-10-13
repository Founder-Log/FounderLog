from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1)
    slug: str = Field(..., min_length=1)
    
    @field_validator("name", "slug")
    @classmethod
    def prevent_empty_spaces(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be empty or contain only spaces")
        return v.strip()


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None=None
    slug: str | None=None

    @field_validator("name", "slug")
    @classmethod
    def prevent_empty_spaces(cls, v: str) -> str:
        if v is None:
            return v

        if not v.strip():
            raise ValueError("Field cannot be empty or contain only spaces")

        return v.strip()


class CategoryResponse(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)