from typing import List

from loguru import logger

from app.core.database import async_session_factory
from app.models.company import CompanyModel
from app.models.job import JobModel, job_technology_association
from app.models.technology import TechnologyModel
from app.repositories.job_repository import JobRepository
from app.scrapers.base import BaseScraper, ScrapedJob


class SyncService:
    def __init__(self, scrapers: List[BaseScraper]):
        self.scrapers = scrapers

    async def sync_all(self) -> dict:
        results = {"created": 0, "updated": 0, "errors": 0, "sources": {}}

        for scraper in self.scrapers:
            try:
                scraped_jobs = await scraper.fetch()
                created, updated = await self._process_jobs(scraped_jobs, scraper.source_name)
                results["created"] += created
                results["updated"] += updated
                results["sources"][scraper.source_name] = {"created": created, "updated": updated}
                logger.info(f"Sync {scraper.source_name}: {created} created, {updated} updated")
            except Exception as e:
                logger.error(f"Sync error for {scraper.source_name}: {str(e)}")
                results["errors"] += 1
                results["sources"][scraper.source_name] = {"error": str(e)}

        return results

    async def _process_jobs(self, scraped_jobs: List[ScrapedJob], source: str) -> tuple:
        created = 0
        updated = 0

        async with async_session_factory() as session:
            repo = JobRepository(session)

            for scraped in scraped_jobs:
                existing = None
                if scraped.external_id:
                    existing = await repo.find_by_external_id(source, scraped.external_id)

                company = await self._get_or_create_company(session, scraped.company_name, scraped.company_logo)

                if existing:
                    changed = await self._update_job_fields(existing, scraped, company)
                    if changed:
                        await repo.update(existing)
                        updated += 1
                else:
                    techs = await self._get_or_create_technologies(session, scraped.technologies)
                    job = JobModel(
                        external_id=scraped.external_id,
                        source=source,
                        title=scraped.title,
                        company_id=company.id,
                        description=scraped.description,
                        requirements=scraped.requirements,
                        benefits=scraped.benefits,
                        city=scraped.city,
                        state=scraped.state,
                        modality=scraped.modality,
                        contract_type=scraped.contract_type,
                        level=scraped.level,
                        salary_min=scraped.salary_min,
                        salary_max=scraped.salary_max,
                        currency=scraped.currency,
                        published_at=scraped.published_at,
                        application_url=scraped.application_url,
                        is_active=True,
                    )
                    job.technologies = techs
                    session.add(job)
                    created += 1

            await session.commit()

        return created, updated

    async def _get_or_create_company(self, session, name: str, logo_url: str | None = None) -> CompanyModel:
        from sqlalchemy import select
        query = select(CompanyModel).where(CompanyModel.name == name)
        result = await session.execute(query)
        company = result.scalar_one_or_none()
        if not company:
            company = CompanyModel(name=name, logo_url=logo_url)
            session.add(company)
            await session.flush()
        return company

    async def _get_or_create_technologies(self, session, tech_names: list[str]) -> list:
        if not tech_names:
            return []
        from sqlalchemy import select
        techs = []
        for tech_name in tech_names:
            query = select(TechnologyModel).where(TechnologyModel.name == tech_name)
            result = await session.execute(query)
            tech = result.scalar_one_or_none()
            if not tech:
                tech = TechnologyModel(name=tech_name)
                session.add(tech)
                await session.flush()
            techs.append(tech)
        return techs

    async def _update_job_fields(self, job: JobModel, scraped: ScrapedJob, company: CompanyModel) -> bool:
        changed = False
        fields = {
            "title": scraped.title,
            "description": scraped.description,
            "requirements": scraped.requirements,
            "benefits": scraped.benefits,
            "city": scraped.city,
            "state": scraped.state,
            "modality": scraped.modality,
            "contract_type": scraped.contract_type,
            "level": scraped.level,
            "salary_min": scraped.salary_min,
            "salary_max": scraped.salary_max,
            "currency": scraped.currency,
            "application_url": scraped.application_url,
            "company_id": company.id,
        }
        for field, value in fields.items():
            if getattr(job, field) != value:
                setattr(job, field, value)
                changed = True
        return changed
