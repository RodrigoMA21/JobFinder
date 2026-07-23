from typing import List, Optional

from pydantic import BaseModel, Field

from app.domain.enums import ContractType, Level, Modality


class JobSearchFilters(BaseModel):
    title: Optional[str] = Field(None, description="Search by job title")
    company: Optional[str] = Field(None, description="Search by company name")
    technology: Optional[str] = Field(None, description="Search by technology name")
    city: Optional[str] = Field(None, description="Search by city")
    state: Optional[str] = Field(None, description="Filter by state")
    modality: Optional[Modality] = Field(None, description="Filter by modality")
    contract_type: Optional[ContractType] = Field(None, description="Filter by contract type")
    level: Optional[Level] = Field(None, description="Filter by experience level")
    salary_min: Optional[float] = Field(None, ge=0, description="Minimum salary filter")
    salary_max: Optional[float] = Field(None, ge=0, description="Maximum salary filter")

    sort_by: Optional[str] = Field("published_at", description="Sort field: published_at, salary_min, salary_max")
    sort_order: Optional[str] = Field("desc", description="Sort order: asc or desc")

    page: int = Field(1, ge=1, description="Page number")
    per_page: int = Field(20, ge=1, le=100, description="Items per page")


class FilterOptions(BaseModel):
    modalities: List[Modality]
    contract_types: List[ContractType]
    levels: List[Level]
    cities: List[str]
    states: List[str]
    technologies: List[str]
