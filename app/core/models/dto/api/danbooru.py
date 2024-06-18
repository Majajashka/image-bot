import html
from dataclasses import dataclass
from typing import Optional, Collection

from app.core.utils.validate_data import validate_danbooru_request_tags


@dataclass
class DanbooruRequestArgs:
    count: int
    tags: Optional[Collection[str]] = None

    def __post_init__(self):
        if not isinstance(self.count, int):
            raise TypeError(f"Tags should be {self.__annotations__['count']}, not {type(self.count)}")

        if not isinstance(self.tags, Collection) and self.tags is not None:
            raise TypeError(f"Tags should be {self.__annotations__['tags']}, not {type(self.tags)}")

        if self.count <= 0:
            raise ValueError(f"Request count should be positive number, not {self.count}")

        validate_danbooru_request_tags(self.tags)


@dataclass
class DanbooruPostTags:
    general: str
    character: str
    copyright: str
    artist: str
    meta: str

    @property
    def general_tags_html_escape(self):
        return html.escape(self.general)


@dataclass
class DanbooruPostFile:
    url: str
    small_file_url: str
    preview_url: str
    file_size: int
    ext: str

    def url_by_size(self, max_size: int = 10_485_760):
        if self.file_size > max_size:
            return self.small_file_url
        return self.url


@dataclass
class DanbooruPost:
    id: int
    file: DanbooruPostFile
    score: int
    rating: str
    tags: DanbooruPostTags
    md5: str

    def __eq__(self, other):
        if isinstance(other, DanbooruPost):
            return self.id == other.id or self.md5 == other.md5
        return False

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            file=DanbooruPostFile(
                url=data.get('file_url'),
                small_file_url=data.get('large_file_url'),
                preview_url=data.get('preview_url'),
                file_size=data.get('file_size'),
                ext=data.get('file_ext')
            ),
            score=data.get('score'),
            rating=data.get('rating'),
            tags=DanbooruPostTags(
                general=data.get('tag_string_general'),
                character=data.get('tag_string_character'),
                copyright=data.get('tag_string_copyright'),
                artist=data.get('tag_string_artist'),
                meta=data.get('tag_string_meta')
            ),
            md5=data.get('md5')
        )


@dataclass
class DanbooruTags:
    id: int
    name: str
    post_count: int
    category: int
    created_at: str
    updated_at: str
    is_deprecated: bool
    words: list

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            post_count=data.get('post_count'),
            category=data.get('category'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            is_deprecated=data.get('is_deprecated'),
            words=data.get('words')

        )
