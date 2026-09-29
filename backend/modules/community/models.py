from datetime import datetime
from enum import Enum

from sqlalchemy import ARRAY, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.db import Base


class ProjectStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"


class Project(Base):
    __tablename__ = "community_projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )

    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)

    status: Mapped[str] = mapped_column(
        String(16), default=ProjectStatus.DRAFT.value, server_default=ProjectStatus.DRAFT.value, index=True
    )

    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String(64)), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
