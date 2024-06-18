from dataclasses import dataclass
from typing import Optional, Collection

from app.core.utils.validate_data import validate_danbooru_request_tags


@dataclass
class DanbooruPostRequestArgs:
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
class DanbooruTagsRequestArgs:
    tags: Optional[str]
