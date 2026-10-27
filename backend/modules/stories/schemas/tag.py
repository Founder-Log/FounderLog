from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional


class TagBase(BaseModel):
    name: str = Field(..., min_length=1)
        
    @field_validator("name")
    @classmethod
    def prevent_empty_spaces(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be empty or contain only spaces")
        return v.strip()


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: str | None=None
    
    @field_validator("name")
    @classmethod
    def prevent_empty_spaces(cls, v: str) -> str:
        if v is None:
            return v
    
        if not v.strip():
            raise ValueError("Field cannot be empty or contain only spaces")
    
        return v.strip()


class TagResponse(TagBase):
    id: int

    model_config = ConfigDict(from_attributes=True)