from datetime import datetime
from sqlalchemy import String, Text, Boolean, Table, Column, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.db import Base


story_tags = Table(
    "story_tags",
    Base.metadata,
    Column("story_id", ForeignKey("stories.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)


class Story(Base):
    __tablename__ = "stories"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    origin_url: Mapped[str] = mapped_column(String(512), nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)

    category: Mapped["Category"] = relationship(back_populates="stories")
    tags: Mapped[list["Tag"]] = relationship(secondary=story_tags, back_populates="stories")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True)

    stories: Mapped[list["Story"]] = relationship(back_populates="category")


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True)

    stories: Mapped[list["Story"]] = relationship(secondary=story_tags, back_populates="tags")   