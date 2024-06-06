from typing import Optional, Collection

from app.core.models.dto.api.danbooru import DanbooruRequestArgs


def parse_args_for_post(
        args: Optional[str],
        default_count: int = 1,
        default_tags: Optional[Collection[str]] = None
) -> DanbooruRequestArgs:
    if not args:
        return DanbooruRequestArgs(count=default_count, tags=default_tags)
    if not default_tags:
        default_tags = []

    arguments = args.split()
    if arguments[0].isdigit():
        count = int(arguments[0])
        if count > 10:
            raise ValueError('The number of requests should not exceed 10')
        tags = arguments[1:]
    else:
        count = default_count
        tags = arguments

    return DanbooruRequestArgs(count=count, tags=set(tags+default_tags))
