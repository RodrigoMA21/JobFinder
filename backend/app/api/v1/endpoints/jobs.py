import math
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.v1.schemas.responses import StandardResponse
from app.domain.enums import ContractType, Level, Modality
from app.schemas.job import JobDetail, JobSummary
from app.schemas.filters import FilterOptions
from app.schemas.responses import PaginatedResponse, PaginationMeta, SingleResponse
from app.scrapers.adzuna import AdzunaScraper
from app.scrapers.findwork import FindworkScraper
from app.scrapers.remotive import RemotiveScraper
from app.services.job_service import JobService
from app.services.sync_service import SyncService
from app.core.dependencies import get_job_service

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("")
async def list_jobs(
    title: Optional[str] = Query(None, description="Search by job title"),
    company: Optional[str] = Query(None, description="Search by company name"),
    technology: Optional[str] = Query(None, description="Search by technology"),
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state"),
    modality: Optional[Modality] = Query(None, description="Filter by modality"),
    contract_type: Optional[ContractType] = Query(None, description="Filter by contract type"),
    level: Optional[Level] = Query(None, description="Filter by experience level"),
    salary_min: Optional[float] = Query(None, ge=0, description="Minimum salary"),
    salary_max: Optional[float] = Query(None, ge=0, description="Maximum salary"),
    sort_by: str = Query("published_at", description="Sort field"),
    sort_order: str = Query("desc", description="Sort order: asc or desc"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    service: JobService = Depends(get_job_service),
):
    items, total = await service.search_jobs(
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

    return PaginatedResponse(
        data=[JobSummary.model_validate(job) for job in items],
        meta=PaginationMeta(
            page=page,
            per_page=per_page,
            total=total,
            total_pages=math.ceil(total / per_page) if total > 0 else 0,
        ),
    )


@router.get("/filters")
async def get_filters(
    service: JobService = Depends(get_job_service),
):
    options = await service.get_filter_options()
    return StandardResponse(data=FilterOptions(**options))


@router.post("/sync")
async def sync_jobs():
    scrapers = [RemotiveScraper(), AdzunaScraper(), FindworkScraper()]
    service = SyncService(scrapers)
    result = await service.sync_all()
    return StandardResponse(data=result)


@router.get("/{job_id}")
async def get_job(
    job_id: UUID,
    service: JobService = Depends(get_job_service),
):
    job = await service.get_job_detail(job_id)
    return SingleResponse(data=JobDetail.model_validate(job))
