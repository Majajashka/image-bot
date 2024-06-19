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
        admins = await bot.get_chat_administrators(message.chat.id)
        admins_id = {admin.user.id for admin in admins}
        return message.from_user.id in admins_id
