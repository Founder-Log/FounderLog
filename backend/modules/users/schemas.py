from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr
    handle: str = Field(min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_.]+$")
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    handle: str
    avatar_url: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class FavoriteToggleRequest(BaseModel):
    target_type: str = Field(description='Пока только "story", позже "project"')
    target_id: int


class FavoriteToggleResponse(BaseModel):
    favorited: bool


class FavoritesListResponse(BaseModel):
    target_type: str
    target_ids: list[int]
