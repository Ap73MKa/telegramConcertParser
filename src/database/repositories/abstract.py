from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Generic, TypeVar

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import BaseModel

AbstractModel = TypeVar("AbstractModel")


class Repository(Generic[AbstractModel], ABC):
    type_model: type[BaseModel]
    session: AsyncSession

    def __init__(self, type_model: type[BaseModel], session: AsyncSession):
        self.type_model = type_model
        self.session = session

    async def get(self, ident: int | str) -> AbstractModel:
        return await self.session.get(entity=self.type_model, ident=ident)

    async def get_by_where(self, where_clause) -> AbstractModel | None:
        statement = select(self.type_model).where(where_clause)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_many(
        self, where_clause=None, limit: int = 128, order_by=None
    ) -> Sequence[AbstractModel]:
        statement = select(self.type_model)
        if where_clause:
            statement = statement.where(where_clause)
        statement = statement.limit(limit).order_by(order_by)
        return (await self.session.scalars(statement)).all()

    async def delete(self, where_clause) -> None:
        statement = delete(self.type_model).where(where_clause)
        await self.session.execute(statement)

    async def insert(self, data) -> None:
        statement = insert(self.type_model).on_conflict_do_nothing()
        await self.session.execute(statement, data)

    @abstractmethod
    async def new(self, *args, **kwargs) -> AbstractModel:
        pass
