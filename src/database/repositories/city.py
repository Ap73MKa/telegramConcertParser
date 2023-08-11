import re

from rapidfuzz.process import extractOne
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import City
from src.database.repositories.abstract import Repository


class CityRepository(Repository[City]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=City, session=session)

    async def new(self, name: str, abb: str, simplified_name: str) -> City:
        new_user = await self.session.merge(
            City(abb=abb, name=name, simplified_name=simplified_name)
        )
        return new_user

    async def fuzzy_get_by_name(self, name: str) -> City | None:
        simplified_cities = [city.simplified_name for city in await self.get_many()]
        simplified_name = re.sub(
            "[^a-zA-Zа-яА-Я]", "", name.lower().strip().replace("ё", "е")
        )
        close = extractOne(simplified_name, simplified_cities)
        min_close_factor = 80
        if close[1] < min_close_factor:
            return None
        return await self.get_by_where(City.simplified_name == str(close[0]))
