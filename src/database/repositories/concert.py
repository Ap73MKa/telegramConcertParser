from datetime import date

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Concert
from src.database.repositories.abstract import Repository


class ConcertRepository(Repository[Concert]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Concert, session=session)

    async def new(
        self,
        name: str,
        link: str,
        price: int,
        concert_date: date,
        city_id: int,
    ) -> Concert:
        new_user = await self.session.merge(
            Concert(
                name=name,
                link=link,
                price=price,
                concert_date=concert_date,
                city_id=city_id
            )
        )
        return new_user

    async def delete_outdated(self) -> None:
        statement = delete(self.type_model).where(Concert.concert_date < date.today())
        await self.session.execute(statement)
