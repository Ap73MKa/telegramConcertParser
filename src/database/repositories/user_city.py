from collections.abc import Sequence

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import City, UserCity
from src.database.repositories.abstract import Repository


class UserCityRepository(Repository[UserCity]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=UserCity, session=session)

    async def new(self, user_id: int, city_id: int) -> UserCity:
        # Check if the user already has a record with the given city
        existing_record = await self.get_by_where(and_(UserCity.user_id == user_id, UserCity.city_id == city_id))
        if existing_record:
            await self.delete(UserCity.id == existing_record.id)

        # Check if the user already has 8 records
        max_city_count = 8
        user_records = await self.get_many(
            where_clause=UserCity.user_id == user_id,
            order_by=UserCity.update_date.desc(),
        )
        if len(user_records) >= max_city_count:
            last_record = user_records[len(user_records) - 1]
            await self.delete(UserCity.id == last_record.id)

        return await self.session.merge(UserCity(user_id=user_id, city_id=city_id))

    async def get_cities_of_user(self, user_id: int) -> Sequence[City]:
        statement = (
            select(City)
            .join(UserCity.city)
            .where(UserCity.user_id == user_id)
            .order_by(UserCity.update_date.desc())
        )
        result = await self.session.scalars(statement)
        return result.all()
