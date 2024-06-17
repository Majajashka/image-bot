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
            insert(DanbooruOrm)
            .values(tg_id=user_id)
            .on_conflict_do_nothing()
            .returning(DanbooruOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one().to_dto()
