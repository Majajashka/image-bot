from typing import Collection, Optional

from app.core.models.dto.api.danbooru import DanbooruPost, DanbooruRequestArgs
from app.core.external_service.api.danbooru import DanbooruAPI
from app.core.models.dto.api.parse_config import ParseConfig
from app.core.utils.expections import UserArgumentError
from app.core.utils.parse_args import parse_args_for_post


class DanbooruRequest:
    pass


async def parse_user_danbooru_args(user_args: str, parse_config: ParseConfig) -> DanbooruRequestArgs:
    try:
        parsed_args = parse_args_for_post(user_args=user_args)
    except ValueError as e:
        raise UserArgumentError(f'Invalid arguments: {e}', user_args=user_args) from e
    if parsed_args.count > parse_config.max_count:
        raise UserArgumentError(
            message="The number of requests shouldn't exceed 10",
            user_args=user_args
        )
    return parsed_args


async def get_danbooru_post(tags: Optional[Collection[str]] = None) -> DanbooruPost:
    danbooru = DanbooruAPI()
    post = await danbooru.image(tags)
    await danbooru.session_close()
    return post
