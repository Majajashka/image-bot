from app.core.models.dto.base import Base


class DanbooruDisplaySettings(Base):
    tags: bool
    score: bool
    rating: bool
    url: bool

    def __repr__(self):
        return f'DanbooruDisplaySettings({self.tags=}, {self.score=}, {self.rating=}, {self.url=})'

    def __str__(self):
        return f'Display settings - Tags: {self.tags}, Score: {self.score}, Rating: {self.rating}, URL: {self.url}'

class UserDanbooruSettings(Base):
    default_tags: str
    default_count: int
    display: DanbooruDisplaySettings

    def __repr__(self):
        return f'UserDanbooruSettings({self.default_tags=}, {self.default_count=}, {repr(self.display)}'

    def __str__(self):
        return (f'User Settings - Default Tags: {self.default_tags}, Default Count: {self.default_count}, '
                f'Display: {str(self.display)}')

    @property
    def default_tags_list(self):
        return self.default_tags.split()
