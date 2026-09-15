from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.db import Base


class Story(Base):
    __tablename__ = "stories"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)