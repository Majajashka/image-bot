from app.core.models.dto.base import Base


class DanbooruDisplaySettings(Base):
    tags: bool
    score: bool
    rating: bool
    url: bool

    def __repr__(self):
        return f'DanbooruDisplaySettings({self.tags=}, {self.score=}, {self.rating=}, {self.url=}'


class UserDanbooruSettings(Base):
    default_tags: str
    default_count: int
    display: DanbooruDisplaySettings

    def __repr__(self):
        return f'UserDanbooruSettings({self.default_tags=}, {self.default_count=}, {repr(self.display)}'
