from typing import Collection, Optional

from sqlalchemy.exc import NoResultFound

from app.core.models.dto.api.danbooru import (
    DanbooruPost,
    DanbooruPostRequestArgs,
    DanbooruTags,
    DanbooruTagsRequestArgs
)
from app.core.external_service.api.danbooru import DanbooruAPI
from app.core.models.dto.api.danbooru import PostParseConfig
from app.core.models.dto.danbooru import UserDanbooruSettings
from app.core.utils.expections import UserArgumentError, InvalidRequestCount
from app.core.utils.parse_args import parse_args_for_post, parse_args_for_tags_search
from app.core.utils.validate_response import validate_danbooru_post
from app.infrastructure.database.repo.danbooru import DanbooruRepo


def parse_user_danbooru_post_args(user_args: str, parse_config: PostParseConfig) -> DanbooruPostRequestArgs:
    try:
        parsed_args = parse_args_for_post(
            user_args=user_args,
            default_count=parse_config.default_count,
            default_tags=parse_config.default_tags
        )
    except ValueError as e:
        raise UserArgumentError(f'Invalid arguments: {e}', user_args=user_args) from e
    if parsed_args.count > parse_config.max_count:
        raise InvalidRequestCount(
            message=f"The number of requests shouldn't exceed {parse_config.max_count}",
            user_args=user_args,
            count=parsed_args.count,
            max_count=parse_config.max_count
        )
    return parsed_args


def parse_user_danbooru_tags_args(user_args: str) -> DanbooruTagsRequestArgs:
    tags = parse_args_for_tags_search(user_args)
    return DanbooruTagsRequestArgs(tags=tags)


async def get_danbooru_post(tags: Optional[Collection[str]] = None) -> DanbooruPost:
    async with DanbooruAPI() as api:
        post = await api.random_image(tags)
    validated_post = validate_danbooru_post(post)
    return validated_post


async def get_or_create_user_danbooru(user_id: int, repo: DanbooruRepo) -> UserDanbooruSettings:
    try:
        user_danbooru = await repo.get_by_id(user_id)
    except NoResultFound:
        user_danbooru = await repo.create_for_user(user_id)
    await repo.session.commit()
    return user_danbooru


async def search_tags(tag: Optional[Collection[str]]) -> list[DanbooruTags]:
    async with DanbooruAPI() as api:
        tags = await api.search_tags(tag=tag)
    return tags
