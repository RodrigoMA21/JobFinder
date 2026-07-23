from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from app.core.config import settings
from app.scrapers.adzuna import AdzunaScraper
from app.scrapers.findwork import FindworkScraper
from app.scrapers.remotive import RemotiveScraper
from app.services.sync_service import SyncService


async def sync_jobs_job():
    logger.info("Starting scheduled job synchronization")
    scrapers = [RemotiveScraper(), AdzunaScraper(), FindworkScraper()]
    service = SyncService(scrapers)
    result = await service.sync_all()
    logger.info(f"Sync completed: {result}")


def create_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        sync_jobs_job,
        "interval",
        hours=settings.SYNC_INTERVAL_HOURS,
        id="sync_jobs",
        name="Sync jobs from external APIs",
        next_run_time=datetime.now(),
        misfire_grace_time=3600,
    )

    return scheduler
