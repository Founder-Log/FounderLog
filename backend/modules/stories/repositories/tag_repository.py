from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.modules.stories.models import Tag
from backend.modules.stories.schemas import TagCreate, TagUpdate


class TagRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_tag_by_name(self, name: str) -> Tag | None:
        query = select(Tag).where(Tag.name == name)
        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def get_tag_by_id(self, tag_id: int) -> Tag | None:
        query = select(Tag).where(Tag.id == tag_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all_tags(self) -> Sequence[Tag]:
        query = select(Tag).order_by(Tag.id.desc())
        result = await self.db.execute(query)

        return result.scalars().all()

    async def create_tag(self, tag_in: TagCreate) -> Tag:
        tag = Tag(**tag_in.model_dump())

        self.db.add(tag)
        await self.db.commit()
        await self.db.refresh(tag)

        return tag

    async def tag_update(self, tag: Tag, data: TagUpdate) -> Tag:
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(tag, field, value)

        await self.db.commit()
        await self.db.refresh(tag)
        return tag 

    async def tag_delete(self, tag: Tag) -> None:
        await self.db.delete(tag)
        await self.db.commit()