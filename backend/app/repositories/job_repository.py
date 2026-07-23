from datetime import datetime
from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy import Select, asc, desc, func, or_, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.domain.enums import ContractType, Level, Modality
from app.models.company import CompanyModel
from app.models.job import JobModel, job_technology_association
from app.models.technology import TechnologyModel
from app.repositories.base import BaseRepository


class JobRepository(BaseRepository[JobModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, JobModel)

    async def find_by_external_id(self, source: str, external_id: str) -> Optional[JobModel]:
        query = select(JobModel).where(
            JobModel.source == source,
            JobModel.external_id == external_id,
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def search(
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
        query = (
            select(JobModel)
            .options(
                joinedload(JobModel.company),
                joinedload(JobModel.technologies),
            )
            .where(JobModel.is_active == True)
        )

        if title:
            query = query.where(JobModel.title.ilike(f"%{title}%"))
        if company:
            query = query.join(CompanyModel).where(
                CompanyModel.name.ilike(f"%{company}%")
            )
        if technology:
            query = (
                query.join(job_technology_association)
                .join(TechnologyModel)
                .where(TechnologyModel.name.ilike(f"%{technology}%"))
            )
        if city:
            query = query.where(JobModel.city.ilike(f"%{city}%"))
        if state:
            query = query.where(JobModel.state.ilike(f"%{state}%"))
        if modality:
            query = query.where(JobModel.modality == modality)
        if contract_type:
            query = query.where(JobModel.contract_type == contract_type)
        if level:
            query = query.where(JobModel.level == level)
        if salary_min is not None:
            query = query.where(JobModel.salary_max >= salary_min)
        if salary_max is not None:
            query = query.where(JobModel.salary_min <= salary_max)

        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar() or 0

        sort_column = getattr(JobModel, sort_by, JobModel.published_at)
        order_func = desc if sort_order == "desc" else asc
        query = query.order_by(order_func(sort_column), JobModel.id.desc())

        offset = (page - 1) * per_page
        query = query.offset(offset).limit(per_page)

        result = await self.session.execute(query)
        items = list(result.unique().scalars().all())

        return items, total

    async def get_filter_options(self) -> dict:
        cities_query = select(JobModel.city).where(
            JobModel.city.isnot(None), JobModel.is_active == True
        ).distinct().order_by(JobModel.city)
        states_query = select(JobModel.state).where(
            JobModel.state.isnot(None), JobModel.is_active == True
        ).distinct().order_by(JobModel.state)
        techs_query = select(TechnologyModel.name).order_by(TechnologyModel.name)

        cities_result = await self.session.execute(cities_query)
        states_result = await self.session.execute(states_query)
        techs_result = await self.session.execute(techs_query)

        return {
            "cities": [row[0] for row in cities_result if row[0]],
            "states": [row[0] for row in states_result if row[0]],
            "technologies": [row[0] for row in techs_result],
        }

    async def find_with_details(self, job_id: UUID) -> Optional[JobModel]:
        query = (
            select(JobModel)
            .options(
                joinedload(JobModel.company),
                joinedload(JobModel.technologies),
            )
            .where(JobModel.id == job_id)
        )
        result = await self.session.execute(query)
        return result.unique().scalar_one_or_none()
