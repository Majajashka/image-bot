from logging import getLogger

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from app.infrastructure.database.holder import HolderRepo
from app.core.utils.parse_args import parse_args_for_post
from app.core.service.danbooru import get_danbooru_post
from app.core.external_service.api.expections import ApiError

router = Router(name=__name__)
logger = getLogger(name=__name__)


@router.message(Command('danbooru'))
async def danbooru_images(message: Message, command: CommandObject):
    try:
        post_args = parse_args_for_post(args=command.args)
    except ValueError as e:
        logger.debug(f'Danbooru argument parse exception: {e.__str__()}')
        await message.answer(e.__str__())
        return

    for _ in range(post_args.count):
        try:
            post = await get_danbooru_post(post_args.tags)
            await message.answer_photo(caption=post.tags.general, photo=post.file.url)
        except (ApiError, ValueError) as e:
            logger.info(e.__str__)
            await message.answer(e.__str__())
