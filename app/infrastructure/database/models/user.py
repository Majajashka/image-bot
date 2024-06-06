from sqlalchemy import BigInteger, true
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.dto.user import User
from app.infrastructure.database.models.base import Base, TimestampMixin


class UserOrm(Base, TimestampMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    active: Mapped[bool] = mapped_column(server_default=true())
    language: Mapped[str] = mapped_column(default='ru')

    def __repr__(self):
        return (f'User(id={self.id}, active={self.active}, language={self.language},'
                f' created_at={self.created_at.strftime("%Y-%m-%d %H:%M:%S")},'
                f' updated_at={self.updated_at.strftime("%Y-%m-%d %H:%M:%S")})')

    def to_dto(self) -> User:
        return User(
            id=self.id,
            active=self.active,
            language=self.language,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
