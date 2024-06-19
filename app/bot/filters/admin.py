from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.types import Message, ChatMemberOwner, ChatMemberAdministrator

from app.bot.config import Config


class IsAdmin(BaseFilter):

    async def __call__(self, message: Message, config: Config) -> bool:
        return message.from_user.id in config.tg_bot.admin_ids


class IsChatAdmin(BaseFilter):
    async def __call__(self, message: Message, bot: Bot) -> bool:
        if message.chat.type == 'private':
            return False
        member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        if isinstance(member, (ChatMemberAdministrator, ChatMemberOwner)):
            return True
        return False
