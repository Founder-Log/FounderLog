from pydantic import BaseModel
from typing import List, Optional


class SearchTagResponse(BaseModel):
    id: int
    name: str
    slug: str

    class Config:
        from_attributes = True


class SearchStoryResponse(BaseModel):
    id: int
    title: str
    content: Optional[str] = None

    class Config:
        from_attributes = True


class SearchCategoryResponse(BaseModel):
    id: int
    name: str
    slug: str

    class Config:
        from_attributes = True


class ClobalSearchResponse(BaseModel):
    query: str
    tags: List[SearchTagResponse] = []
    stories: List[SearchStoryResponse] = []
    categories: List[SearchCategoryResponse] = []