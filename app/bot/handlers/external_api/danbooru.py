from logging import getLogger

from aiogram import Router, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, URLInputFile, CallbackQuery
from fluentogram import TranslatorRunner

from app.core.models.dto.api.danbooru.parse_config import PostParseConfig
from app.core.service.danbooru import (
    get_danbooru_post,
    search_tags,
    parse_user_danbooru_post_args,
    get_or_create_user_danbooru,
    parse_user_danbooru_tags_args
)
from app.core.service.user import get_or_create_user
from app.core.utils.expections import InvalidDanbooruPostData
from app.infrastructure.database.holder import HolderRepo
from app.core.constants.danbooru import MAX_ADMIN_POST_COUNT
from app.bot.keyboards.binded_chat import danbooru_post_inline_kb, BindedChatCallbackFactory

router = Router(name=__name__)
logger = getLogger(name=__name__)


@router.message(Command('danbooru'))
async def danbooru_images(
        message: Message,
        command: CommandObject,
        i18n: TranslatorRunner,
        repo: HolderRepo
):
    danbooru_user = await get_or_create_user_danbooru(user_id=message.from_user.id, repo=repo.danbooru)
    logger.info(danbooru_user)
    post_args = parse_user_danbooru_post_args(
        user_args=command.args,
        parse_config=PostParseConfig(
            max_count=MAX_ADMIN_POST_COUNT,
            default_tags=danbooru_user.default_tags_list,
            default_count=danbooru_user.default_count
        )
    )
    logger.info(f'Posts for User: {message.from_user.full_name}, id: {message.from_user.id}, {post_args}')

    error_count = 0
    for _ in range(post_args.count):
        try:
            post = await get_danbooru_post(post_args.tags)
            await message.answer_photo(
                caption=i18n.danbooru.post(
                    tags=post.tags.general_tags_html_escape if danbooru_user.display.tags else False,
                    url=post.file.url if danbooru_user.display.url else False,
                    score=post.score if danbooru_user.display.score else False,
                    rating=post.rating if danbooru_user.display.rating else False
                ),
                photo=URLInputFile(url=post.file.url_by_size()),
                reply_markup=danbooru_post_inline_kb(
                    user_id=message.from_user.id,
                    message_id=message.message_id,
                    chat_id=message.chat.id
                )
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


@router.message(Command('search'))
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


@router.callback_query(BindedChatCallbackFactory.filter())
async def resend_photo(
        callback: CallbackQuery,
        callback_data: BindedChatCallbackFactory,
        bot: Bot,
        repo: HolderRepo,
        l18n: TranslatorRunner
):
    user = await get_or_create_user(tg_id=callback.from_user.id, repo=repo.users)
    if user.binded_chat is None:
        await callback.answer(l18n.error.chat_bind())
        return
    await bot.copy_message(
        chat_id=user.binded_chat,
        from_chat_id=callback_data.chat_id,
        message_id=callback_data.message_id)
