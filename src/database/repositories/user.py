from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.database.repositories.abstract import Repository


class UserRepository(Repository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=User, session=session)

    async def new(
        self,
        user_id: int,
        user_name: str | None = None,
    ) -> User:
        new_user = User(user_id=user_id, full_name=user_name)
        return await self.session.merge(new_user)

    async def update_page(self, user_id: int, page: int) -> None:
        statement = (
            update(self.type_model)
            .where(User.user_id == user_id)
            .values(city_page=page)
        )
        await self.session.execute(statement)
