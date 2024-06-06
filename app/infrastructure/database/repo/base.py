from sys import platform

from typing import TypeVar, Generic

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.base import Base
from app.infrastructure.database.models.user import UserOrm

if platform == 'win32':
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

Model = TypeVar('Model', bound=Base, covariant=True, contravariant=False)


class BaseRepo(Generic[Model]):
    """
    A class representing a base repository for handling database operations.

    Attributes:
        session (AsyncSession): The database session used by the repository.
        model (Model): The database table model.
    """

    def __init__(self, session: AsyncSession, model: type[Model]) -> None:
        self.session: AsyncSession = session
        self.model = model

    async def _get_by_id(self, user_id: int) -> UserOrm:
        r = await self.session.get(
            self.model,
            user_id,
        )
        if r is None:
            raise NoResultFound
        return r

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
