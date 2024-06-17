from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.repo.danbooru import DanbooruRepo
from app.infrastructure.database.repo.user import UserRepo


class HolderRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    @property
    def users(self):
        return UserRepo(session=self.session)

    @property
    def danbooru(self):
        return DanbooruRepo(session=self.session)
