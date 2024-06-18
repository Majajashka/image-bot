from logging import getLogger

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, URLInputFile
from fluentogram import TranslatorRunner

from app.core.models.dto.api.danbooru.parse_config import PostParseConfig
from app.core.service.danbooru import (
    get_danbooru_post,
    search_tags,
    parse_user_danbooru_post_args,
    get_or_create_user_danbooru,
    parse_user_danbooru_tags_args
)
from app.core.utils.expections import InvalidDanbooruPostData
from app.infrastructure.database.holder import HolderRepo
from app.core.constants.danbooru import MAX_ADMIN_POST_COUNT

router = Router(name=__name__)
logger = getLogger(name=__name__)


@router.message(Command('danbooru'))
async def danbooru_images(
        message: Message,
        command: CommandObject,
        i18n: TranslatorRunner,
        repo: HolderRepo
):
    user = await get_or_create_user_danbooru(user_id=message.from_user.id, repo=repo.danbooru)
    logger.info(user)
    post_args = parse_user_danbooru_post_args(
        user_args=command.args,
        parse_config=PostParseConfig(
            max_count=MAX_ADMIN_POST_COUNT,
            default_tags=user.default_tags_list,
            default_count=user.default_count
        )
    )
    logger.info(f'Posts for User: {message.from_user.full_name}, id: {message.from_user.id}, {post_args}')

    error_count = 0
    for _ in range(post_args.count):
        try:
            post = await get_danbooru_post(post_args.tags)
            await message.answer_photo(
                caption=i18n.danbooru.post(
                    tags=post.tags.general_tags_html_escape if user.display.tags else False,
                    url=post.file.url if user.display.url else False,
                    score=post.score if user.display.score else False,
                    rating=post.rating if user.display.rating else False
                ),
                photo=URLInputFile(url=post.file.url_by_size())
            )
        except InvalidDanbooruPostData as e:
            error_count += 1
            logger.debug(e)
        except TelegramBadRequest as e:
            error_count += 1
            logger.debug(e)
        finally:
            if error_count >= 5:
                await message.answer(text='Too much errors. Aborting...')
                break
            error_count = 0


@router.message(Command('tags'))
async def danbooru_images(
        message: Message,
        command: CommandObject,
        i18n: TranslatorRunner,
):
    parsed_args = parse_user_danbooru_tags_args(user_args=command.args)
    tags = await search_tags(parsed_args.tags)
    text = '\n'.join(
        (i18n.danbooru.tags(tag=tag.name, post_count=tag.post_count) for tag in tags)
    )
    await message.answer(text)