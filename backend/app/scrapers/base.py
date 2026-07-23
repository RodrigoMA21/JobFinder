from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from app.domain.enums import ContractType, Level, Modality


@dataclass
class ScrapedJob:
    external_id: Optional[str]
    title: str
    company_name: str
    company_logo: Optional[str] = None
    description: str = ""
    requirements: Optional[str] = None
    benefits: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    modality: Modality = Modality.REMOTE
    contract_type: ContractType = ContractType.CLT
    level: Level = Level.MID
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: str = "BRL"
    published_at: Optional[datetime] = None
    application_url: Optional[str] = None
    technologies: List[str] = field(default_factory=list)


class BaseScraper(ABC):
    def __init__(self, source_name: str):
        self.source_name = source_name

    @abstractmethod
    async def fetch(self) -> List[ScrapedJob]:
        pass
