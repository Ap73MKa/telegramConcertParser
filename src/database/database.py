from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.pool import NullPool

from .repositories import (
    CityRepository,
    ConcertRepository,
    UserCityRepository,
    UserRepository,
)


def create_async_engine(url: URL | str) -> AsyncEngine:
    return _create_async_engine(
        url=url, echo=False, pool_pre_ping=True, poolclass=NullPool
    )


def create_session_maker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(engine, expire_on_commit=True)


class Database:
    session: AsyncSession
    user: UserRepository
    city: CityRepository
    concert: ConcertRepository
    user_city: UserCityRepository

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.user = UserRepository(session=session)
        self.city = CityRepository(session=session)
        self.concert = ConcertRepository(session=session)
        self.user_city = UserCityRepository(session=session)
