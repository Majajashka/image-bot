from sqlalchemy import BigInteger, true, false
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.dto.user import User
from app.infrastructure.database.models.base import Base, TimestampMixin


class UserOrm(Base, TimestampMixin):
    __tablename__ = 'users'

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    active: Mapped[bool] = mapped_column(server_default=true())
    language: Mapped[str] = mapped_column(default='ru')
    banned: Mapped[bool] = mapped_column(server_default=false())
    binded_chat: Mapped[int] = mapped_column(BigInteger, server_default=None)

    danbooru = relationship('DanbooruOrm', back_populates='user')

    def __repr__(self):
        return (f'User(id={self.tg_id}, active={self.active}, language={self.language},'
                f' created_at={self.created_at.strftime("%Y-%m-%d %H:%M:%S")},'
                f' updated_at={self.updated_at.strftime("%Y-%m-%d %H:%M:%S")})')

    def to_dto(self) -> User:
        return User(
            tg_id=self.tg_id,
            active=self.active,
            language=self.language,
            created_at=self.created_at,
            updated_at=self.updated_at,
            banned=self.banned,
            binded_chat=self.binded_chat
        )
