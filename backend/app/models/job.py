import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, String, Text, Table, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import ContractType, Level, Modality
from app.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.company import CompanyModel
    from app.models.technology import TechnologyModel


job_technology_association = Table(
    "job_technologies",
    Base.metadata,
    Column("job_id", UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"), primary_key=True),
    Column("technology_id", UUID(as_uuid=True), ForeignKey("technologies.id", ondelete="CASCADE"), primary_key=True),
)


class JobModel(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "jobs"

    external_id: Mapped[Optional[str]] = mapped_column(String(255), index=True, nullable=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)

    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False
    )
    company: Mapped["CompanyModel"] = relationship(
        "CompanyModel", back_populates="jobs", lazy="selectin"
    )

    description: Mapped[str] = mapped_column(Text, nullable=False)
    requirements: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    benefits: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(50), index=True, nullable=True)

    modality: Mapped[Modality] = mapped_column(
        Enum(Modality, name="modality_enum", create_constraint=True),
        index=True,
        nullable=False,
    )
    contract_type: Mapped[ContractType] = mapped_column(
        Enum(ContractType, name="contract_type_enum", create_constraint=True),
        index=True,
        nullable=False,
    )
    level: Mapped[Level] = mapped_column(
        Enum(Level, name="level_enum", create_constraint=True),
        index=True,
        nullable=False,
    )

    salary_min: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    salary_max: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String(10), default="BRL", nullable=False)

    published_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), index=True, nullable=True
    )
    application_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    technologies: Mapped[List["TechnologyModel"]] = relationship(
        "TechnologyModel",
        secondary="job_technologies",
        back_populates="jobs",
        lazy="selectin",
    )
