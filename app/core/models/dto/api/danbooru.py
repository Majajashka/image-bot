from dataclasses import dataclass
from typing import Optional, Collection

from app.core.constants.danbooru import FREE_TAGS


@dataclass
class DanbooruRequestArgs:
    count: int
    tags: Optional[Collection[str]] = None

    def __post_init__(self):
        if self.count <= 0:
            raise ValueError("Request count should be positive number.")

        if isinstance(self.tags, Collection):
            priceble_tags_count = 0

            for tag in self.tags:
                if not any(tag.startswith(free_tag) for free_tag in FREE_TAGS):
                    priceble_tags_count += 1

                if priceble_tags_count > 2:
                    # Danbooru API limit
                    raise ValueError("You cannot search for more than 2 tags at a time")


@dataclass
class DanbooruPostTags:
    general: str
    character: str
    copyright: str
    artist: str
    meta: str


@dataclass
class DanbooruPostFile:
    url: str
    small_file_url: str
    preview_url: str


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
                preview_url=data.get('preview_url')
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
