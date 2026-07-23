from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from app.domain.enums import ContractType, Level, Modality


@dataclass
class Company:
    name: str
    logo_url: Optional[str] = None
    website: Optional[str] = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Technology:
    name: str
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Job:
    title: str
    company: Company
    description: str
    modality: Modality
    contract_type: ContractType
    level: Level
    source: str
    published_at: Optional[datetime] = None
    external_id: Optional[str] = None
    requirements: Optional[str] = None
    benefits: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: str = "BRL"
    application_url: Optional[str] = None
    technologies: list[Technology] = field(default_factory=list)
    is_active: bool = True
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
