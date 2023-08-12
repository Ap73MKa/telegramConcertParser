from datetime import date, datetime

from sqlalchemy import DATE, TIMESTAMP, VARCHAR, ForeignKey, Integer, func
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class BaseModel(DeclarativeBase):
    pass


async def process_scheme(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


class User(BaseModel):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        Integer, unique=True, nullable=False, primary_key=True
    )
    full_name: Mapped[str] = mapped_column(VARCHAR(64), nullable=True)
    city_page: Mapped[int] = mapped_column(Integer, default=1)
    reg_date: Mapped[date] = mapped_column(DATE, default=date.today())

    cities: Mapped[list["UserCity"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.user_id} name={self.full_name})"


class City(BaseModel):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(
        Integer, unique=True, nullable=False, primary_key=True
    )
    abb: Mapped[str] = mapped_column(VARCHAR(64), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(VARCHAR(64), unique=True, nullable=False)
    simplified_name: Mapped[str] = mapped_column(
        VARCHAR(64), unique=True, nullable=False
    )

    concerts: Mapped[list["Concert"]] = relationship(back_populates="city")
    users: Mapped[list["UserCity"]] = relationship(back_populates="city")

    def __repr__(self) -> str:
        return f"City(id={self.id} abb:{self.abb})"


class Concert(BaseModel):
    __tablename__ = "concerts"

    id: Mapped[int] = mapped_column(
        Integer, unique=True, nullable=False, primary_key=True
    )
    name: Mapped[str] = mapped_column(VARCHAR(128), nullable=False)
    link: Mapped[str] = mapped_column(VARCHAR(256), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    concert_date: Mapped[date] = mapped_column(DATE, nullable=False)

    city_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("cities.id"), nullable=False
    )
    city: Mapped[City] = relationship(back_populates="concerts")

    add_time: Mapped[date] = mapped_column(DATE, default=date.today())

    def __repr__(self) -> str:
        return f"Concert(id={self.id} city_id={self.city_id} name={self.name})"


class UserCity(BaseModel):
    __tablename__ = "users_cities"

    id: Mapped[int] = mapped_column(
        Integer, unique=True, nullable=False, primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.user_id"), nullable=False
    )
    user: Mapped[User] = relationship(back_populates="cities")

    city_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("cities.id"), nullable=False
    )
    city: Mapped[City] = relationship(back_populates="users")

    update_date: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    def __repr__(self) -> str:
        return f"UserCity(id={self.id} city_id={self.city_id} user_id={self.user_id})"
