from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.job_repository import JobRepository
from app.services.job_service import JobService
from app.services.sync_service import SyncService
from app.scrapers.remotive import RemotiveScraper
from app.scrapers.findwork import FindworkScraper


async def get_job_repository(
    db: AsyncSession = Depends(get_db),
) -> JobRepository:
    return JobRepository(db)


async def get_job_service(
    repo: JobRepository = Depends(get_job_repository),
) -> JobService:
    return JobService(repo)


async def get_sync_service() -> SyncService:
    scrapers = [RemotiveScraper(), FindworkScraper()]
    return SyncService(scrapers)
