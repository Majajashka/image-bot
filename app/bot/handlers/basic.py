import logging

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from fluentogram import TranslatorRunner

from app.core.service.user import get_or_create_user, bind_chat
from app.infrastructure.database.holder import HolderRepo
from app.bot.filters.admin import IsChatAdmin

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def start(message: Message, i18n: TranslatorRunner, repo: HolderRepo):
    await message.answer(i18n.start(name=message.from_user.first_name))
    await get_or_create_user(message.from_user.id, repo.users)


@router.message(IsChatAdmin(), Command('bind_chat'))
async def bind_chat(message: Message, l18n: TranslatorRunner, repo: HolderRepo):
    await bind_chat(user_id=message.from_user.id, chat_id=message.chat.id)
    await message.answer(text=l18n.chat_bind())
