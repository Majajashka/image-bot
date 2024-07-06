from sqlalchemy import update, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.dto.danbooru import UserDanbooruSettings
from app.infrastructure.database.models.danbooru import DanbooruOrm
from app.infrastructure.database.repo.base import BaseRepo


class DanbooruRepo(BaseRepo[DanbooruOrm]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=DanbooruOrm, session=session)

    async def get_by_id(self, tg_id: int) -> UserDanbooruSettings:
        return (await self._get_by_id(tg_id)).to_dto()

    async def create_for_user(self, user_id: int) -> UserDanbooruSettings:
        stmt = (
            insert(self.model)
            .values(tg_id=user_id)
            .on_conflict_do_nothing()
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one().to_dto()

    async def set_default_tags(self, user_id: int, default_tags: str) -> None:
        stmt = (
            update(self.model)
            .where(self.model.tg_id == user_id)
            .values(default_tags=default_tags)
        )
        await self.session.execute(stmt)

    async def set_default_count(self, user_id: int, default_count: int) -> None:
        stmt = (
            update(self.model)
            .where(self.model.tg_id == user_id)
            .values(default_count=default_count)
        )
        await self.session.execute(stmt)

    async def reset_default_tags(self, user_id: int) -> None:
        stmt = (
            update(self.model)
            .where(self.model.tg_id == user_id)
            .values(default_tags=text('DEFAULT'))
        )
        await self.session.execute(stmt)

    async def reset_default_count(self, user_id: int) -> None:
        stmt = (
            update(self.model)
            .where(self.model.tg_id == user_id)
            .values(default_count=text('DEFAULT'))
        )
        await self.session.execute(stmt)
