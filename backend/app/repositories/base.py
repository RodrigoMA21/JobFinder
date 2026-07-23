from typing import Generic, Optional, Type, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model_class: Type[ModelType]):
        self.session = session
        self.model_class = model_class

    async def create(self, **kwargs) -> ModelType:
        instance = self.model_class(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def get_by_id(self, entity_id: UUID) -> Optional[ModelType]:
        query = select(self.model_class).where(self.model_class.id == entity_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update(self, instance: ModelType, **kwargs) -> ModelType:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await self.session.flush()
        return instance

    async def delete(self, instance: ModelType) -> None:
        await self.session.delete(instance)
        await self.session.flush()

    async def exists(self, **filters) -> bool:
        query = select(self.model_class).filter_by(**filters)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None
