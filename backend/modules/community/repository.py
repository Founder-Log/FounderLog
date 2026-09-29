from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.modules.community.models import Project, ProjectStatus


class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, author_id: int, **fields) -> Project:
        project = Project(author_id=author_id, status=ProjectStatus.DRAFT.value, **fields)
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def get(self, project_id: int) -> Project | None:
        return await self.db.get(Project, project_id)

    async def list_published(self, limit: int = 20, offset: int = 0) -> list[Project]:
        result = await self.db.execute(
            select(Project)
            .where(Project.status == ProjectStatus.PUBLISHED.value)
            .order_by(Project.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def list_by_author(
        self, author_id: int, limit: int = 20, offset: int = 0
    ) -> list[Project]:
        result = await self.db.execute(
            select(Project)
            .where(Project.author_id == author_id)
            .order_by(Project.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def save(self, project: Project) -> Project:
        await self.db.commit()
        await self.db.refresh(project)
        return project
