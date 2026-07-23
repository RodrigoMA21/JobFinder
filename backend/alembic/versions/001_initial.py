"""initial

Revision ID: 001
Revises:
Create Date: 2026-07-22 19:30:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), unique=True, index=True, nullable=False),
        sa.Column("logo_url", sa.String(500), nullable=True),
        sa.Column("website", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "technologies",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(100), unique=True, index=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "jobs",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("external_id", sa.String(255), index=True, nullable=True),
        sa.Column("source", sa.String(50), nullable=False),
        sa.Column("title", sa.String(255), index=True, nullable=False),
        sa.Column("company_id", UUID(as_uuid=True), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("requirements", sa.Text, nullable=True),
        sa.Column("benefits", sa.Text, nullable=True),
        sa.Column("city", sa.String(100), nullable=True),
        sa.Column("state", sa.String(50), index=True, nullable=True),
        sa.Column(
            "modality",
            sa.Enum("remote", "hybrid", "onsite", name="modality_enum"),
            index=True,
            nullable=False,
        ),
        sa.Column(
            "contract_type",
            sa.Enum("clt", "pj", "freelancer", "internship", name="contract_type_enum"),
            index=True,
            nullable=False,
        ),
        sa.Column(
            "level",
            sa.Enum("internship", "junior", "mid", "senior", name="level_enum"),
            index=True,
            nullable=False,
        ),
        sa.Column("salary_min", sa.Float, nullable=True),
        sa.Column("salary_max", sa.Float, nullable=True),
        sa.Column("currency", sa.String(10), server_default="BRL", nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), index=True, nullable=True),
        sa.Column("application_url", sa.String(500), nullable=True),
        sa.Column("is_active", sa.Boolean, server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "job_technologies",
        sa.Column("job_id", UUID(as_uuid=True), sa.ForeignKey("jobs.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("technology_id", UUID(as_uuid=True), sa.ForeignKey("technologies.id", ondelete="CASCADE"), primary_key=True),
    )


def downgrade() -> None:
    op.drop_table("job_technologies")
    op.drop_table("jobs")
    op.drop_table("technologies")
    op.drop_table("companies")
    op.execute("DROP TYPE IF EXISTS modality_enum")
    op.execute("DROP TYPE IF EXISTS contract_type_enum")
    op.execute("DROP TYPE IF EXISTS level_enum")
