from typing import Optional, Collection

from app.core.models.dto.api.danbooru import DanbooruPostRequestArgs, DanbooruTagsRequestArgs


def parse_args_for_post(
        user_args: Optional[str],
        default_count: int = 1,
        default_tags: Optional[Collection[str]] = None
) -> DanbooruPostRequestArgs:
    if not user_args:
        return DanbooruPostRequestArgs(count=default_count, tags=default_tags)
    if not default_tags:
        default_tags = []

    arguments = user_args.split()
    if arguments[0].isdigit():
        count = int(arguments[0])
        tags = arguments[1:]
    else:
        count = default_count
        tags = arguments

    tags += default_tags
    return DanbooruPostRequestArgs(count=count, tags=tags)


def parse_args_for_tags_search(user_args: Optional[str]) -> DanbooruTagsRequestArgs:
    if not user_args:
        return DanbooruTagsRequestArgs(tags=None)

    return DanbooruTagsRequestArgs(tags=user_args.split())
