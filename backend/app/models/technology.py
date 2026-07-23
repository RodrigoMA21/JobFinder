from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.job import JobModel


class TechnologyModel(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "technologies"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)

    jobs: Mapped[List["JobModel"]] = relationship(
        "JobModel", secondary="job_technologies", back_populates="technologies", lazy="selectin"
    )
