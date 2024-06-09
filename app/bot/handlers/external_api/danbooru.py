from logging import getLogger

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from fluentogram import TranslatorRunner

from app.core.models.dto.api.parse_config import ParseConfig
from app.core.service.danbooru import parse_user_danbooru_args
from app.core.service.danbooru import get_danbooru_post
from app.core.utils.expections import ApiError
from app.infrastructure.database.holder import HolderRepo

router = Router(name=__name__)
logger = getLogger(name=__name__)


@router.message(Command('danbooru'))
async def danbooru_images(
        message: Message,
        command: CommandObject,
        i18n: TranslatorRunner,
        repo: HolderRepo
):
    post_args = await parse_user_danbooru_args(user_args=command.args, parse_config=ParseConfig(10))

    for _ in range(post_args.count):
        try:
            post = await get_danbooru_post(post_args.tags)
            await message.answer_photo(
                caption=i18n.api.danbooru_post(
                    tags=post.tags.general,
                    url=post.file.url,
                    score=post.score,
                    rating=post.rating
                ),
                photo=post.file.url)
        except (ApiError, ValueError) as e:
            logger.info(e.__str__)
            await message.answer(e.__str__())
