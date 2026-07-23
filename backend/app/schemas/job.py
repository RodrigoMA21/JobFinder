from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import ContractType, Level, Modality


class CompanySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    logo_url: Optional[str] = None
    website: Optional[str] = None


class TechnologySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str


class JobSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    company: CompanySchema
    city: Optional[str] = None
    state: Optional[str] = None
    modality: Modality
    contract_type: ContractType
    level: Level
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: str = "BRL"
    technologies: List[TechnologySchema] = Field(default_factory=list)
    published_at: Optional[datetime] = None
    application_url: Optional[str] = None


class JobDetail(JobSummary):
    description: str
    requirements: Optional[str] = None
    benefits: Optional[str] = None
    source: str
    created_at: datetime
    updated_at: datetime
