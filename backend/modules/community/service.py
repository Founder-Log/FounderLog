from sqlalchemy.ext.asyncio import AsyncSession

from backend.modules.community.models import Project, ProjectStatus
from backend.modules.community.repository import ProjectRepository
from backend.modules.community.schemas import ProjectCreate, ProjectUpdate


class ProjectNotFound(Exception):
    pass


class NotProjectOwner(Exception):
    pass


class ProjectNotEditable(Exception):
    pass


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.repository = ProjectRepository(db)

    async def create_draft(self, author_id: int, data: ProjectCreate) -> Project:
        return await self.repository.create(author_id=author_id, **data.model_dump())

    async def get_visible(self, project_id: int, viewer_id: int | None) -> Project:
        project = await self.repository.get(project_id)
        if project is None:
            raise ProjectNotFound(project_id)

        if project.status == ProjectStatus.DRAFT.value and project.author_id != viewer_id:
            raise ProjectNotFound(project_id)

        return project

    async def list_feed(self, limit: int = 20, offset: int = 0) -> list[Project]:
        return await self.repository.list_published(limit=limit, offset=offset)

    async def list_mine(
        self, author_id: int, limit: int = 20, offset: int = 0
    ) -> list[Project]:
        return await self.repository.list_by_author(
            author_id, limit=limit, offset=offset
        )

    async def update_draft(
        self, project_id: int, editor_id: int, data: ProjectUpdate
    ) -> Project:
        project = await self.repository.get(project_id)
        if project is None:
            raise ProjectNotFound(project_id)
        if project.author_id != editor_id:
            raise NotProjectOwner(project_id)
        if project.status != ProjectStatus.DRAFT.value:
            raise ProjectNotEditable(project_id)

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(project, field, value)

        return await self.repository.save(project)

    async def publish(self, project_id: int, author_id: int) -> Project:
        project = await self.repository.get(project_id)
        if project is None:
            raise ProjectNotFound(project_id)
        if project.author_id != author_id:
            raise NotProjectOwner(project_id)
        if project.status == ProjectStatus.PUBLISHED.value:
            return project 

        project.status = ProjectStatus.PUBLISHED.value
        return await self.repository.save(project)
