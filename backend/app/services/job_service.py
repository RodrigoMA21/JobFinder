from typing import List, Optional, Tuple
from uuid import UUID

from app.domain.enums import ContractType, Level, Modality
from app.models.job import JobModel
from app.repositories.job_repository import JobRepository
from app.core.exceptions import NotFoundException


class JobService:
    def __init__(self, repository: JobRepository):
        self.repository = repository

    async def search_jobs(
        self,
        title: Optional[str] = None,
        company: Optional[str] = None,
        technology: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        modality: Optional[Modality] = None,
        contract_type: Optional[ContractType] = None,
        level: Optional[Level] = None,
        salary_min: Optional[float] = None,
        salary_max: Optional[float] = None,
        sort_by: str = "published_at",
        sort_order: str = "desc",
        page: int = 1,
        per_page: int = 20,
    ) -> Tuple[List[JobModel], int]:
        return await self.repository.search(
            title=title,
            company=company,
            technology=technology,
            city=city,
            state=state,
            modality=modality,
            contract_type=contract_type,
            level=level,
            salary_min=salary_min,
            salary_max=salary_max,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            per_page=per_page,
        )

    async def get_job_detail(self, job_id: UUID) -> JobModel:
        job = await self.repository.find_with_details(job_id)
        if not job:
            raise NotFoundException("Job", str(job_id))
        return job

    async def get_filter_options(self) -> dict:
        options = await self.repository.get_filter_options()
        options["modalities"] = list(Modality)
        options["contract_types"] = list(ContractType)
        options["levels"] = list(Level)
        return options
