from pydantic import BaseModel, ConfigDict


class StoryCreate(BaseModel):
    title: str
    content: str


class StoryResponse(BaseModel):
    id: int
    title: str
    content: str

    model_config = ConfigDict(from_attributes=True)