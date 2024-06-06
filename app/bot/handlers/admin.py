import logging
# from typing import TYPE_CHECKING

from aiogram import Router, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message
from fluentogram import TranslatorRunner

from app.bot.filters.admin import IsAdmin
from app.bot.config import Config
from app.core.service.user import get_users_count_by_status
from app.infrastructure.database.holder import HolderRepo

# if TYPE_CHECKING:
# from bot.language.locales.stubs.stub import TranslatorRunner

logger = logging.getLogger(__name__)
admin_router = Router(name=__name__)

admin_router.message.filter(IsAdmin())
admin_router.callback_query.filter(IsAdmin())


@admin_router.message(Command('total'))
async def total(message: Message, repo: HolderRepo, i18n: TranslatorRunner):
    count = await get_users_count_by_status(repo.users)
    await message.answer(i18n.total(total_users_count=str(count.active+count.inactive),
                                    active_users_count=str(count.active),
                                    inactive_users_count=str(count.inactive)))


@admin_router.message(Command('admin_list'))
async def admin_list(message: Message, config: Config, bot: Bot, i18n: TranslatorRunner):
    admin_ids = config.tg_bot.admin_ids
    admin_lines = []

    for admin_id in admin_ids:
        try:
            user = await bot.get_chat(chat_id=admin_id)
            name = user.first_name
        except TelegramBadRequest:
            name = 'Unknown'

        admin_lines.append(i18n.admin_list(name=name, id=str(admin_id)))

    admin_text = '\n'.join(admin_lines)
    text = (f"<b>{i18n.admins()}:</b>\n\n"
            f"{admin_text}")
    await message.answer(text)
