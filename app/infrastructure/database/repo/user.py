from sqlalchemy import select, func, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.dto.user import User
from app.infrastructure.database.models.user import UserOrm
from app.infrastructure.database.repo.base import BaseRepo


class UserRepo(BaseRepo[UserOrm]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=UserOrm, session=session)

    async def get_user_by_id(self, user_id: int) -> User:
        return (await self._get_by_id(user_id)).to_dto()

    async def upsert_user(self, user: User) -> User:
        stmt = (
            insert(UserOrm)
            .values(tg_id=user.tg_id)
            .on_conflict_do_nothing()
            .returning(UserOrm)
        )

        saved_user = await self.session.execute(stmt)
        return saved_user.scalar_one().to_dto()

    async def get_users_count_by_status(self, status: bool = True) -> int:
        stmt = (
            select(func.count())
            .where(self.model.active == status)
        )
        users = await self.session.execute(stmt)
        count = users.scalars().one()
        return count

    async def bind_chat(self, user_id: int, chat_id: int) -> User:
        stmt = (
            update(self.model)
            .where(self.model.tg_id == user_id)
            .values(binded_chat=chat_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one().to_dto()
