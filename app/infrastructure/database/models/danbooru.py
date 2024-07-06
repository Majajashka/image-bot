from typing import Optional

from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.models.base import Base, TimestampMixin
from app.core.models.dto.danbooru import UserDanbooruSettings, DanbooruDisplaySettings
from app.core.constants.danbooru import USER_DEFAULT_TAGS, USER_DEFAULT_COUNT


class DanbooruOrm(Base, TimestampMixin):
    __tablename__ = 'danbooru'

    tg_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.tg_id'), primary_key=True)
    default_tags: Mapped[Optional[str]] = mapped_column(default=' '.join(USER_DEFAULT_TAGS))
    default_count: Mapped[int] = mapped_column(default=str(USER_DEFAULT_COUNT))
    tags_display: Mapped[bool] = mapped_column(default=True)
    score_display: Mapped[bool] = mapped_column(default=True)
    rating_display: Mapped[bool] = mapped_column(default=True)
    url_display: Mapped[bool] = mapped_column(default=True)

    user = relationship('UserOrm', back_populates='danbooru', uselist=False)

    def to_dto(self) -> UserDanbooruSettings:
        return UserDanbooruSettings(
            default_tags=self.default_tags,
            default_count=self.default_count,
            display=DanbooruDisplaySettings(
                tags=self.tags_display,
                score=self.score_display,
                url=self.url_display,
                rating=self.tags_display
            )
        )
