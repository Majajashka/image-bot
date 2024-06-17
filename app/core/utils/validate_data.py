from typing import Optional, Collection

from app.core.constants.danbooru import FREE_TAGS
from app.core.utils.expections import InvalidTagsCount


def validate_danbooru_request_tags(tags: Optional[Collection[str]], max_tags: int = 2) -> Optional[Collection[str]]:
    if not tags:
        return tags

    priceble_tags_count = 0

    for tag in tags:
        if not any(tag.startswith(free_tag) for free_tag in FREE_TAGS):
            priceble_tags_count += 1

    if priceble_tags_count > max_tags:
        raise InvalidTagsCount(
            message=f"You cannot search for more than {max_tags} tags at a time",
            tags=tags,
            count=priceble_tags_count,
        )

    return tags
