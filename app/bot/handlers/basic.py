import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from fluentogram import TranslatorRunner

from app.core.models.dto.user import User
from app.core.service.user import create_user, get_user_by_id
from app.infrastructure.database.holder import HolderRepo

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def start(message: Message, i18n: TranslatorRunner, repo: HolderRepo):
    await message.answer(i18n.start(name=message.from_user.first_name))

    user = await get_user_by_id(message.from_user.id, repo.users)
    if not user:
        user_dto = User(
            id=message.from_user.id
        )
        user = await create_user(user_dto, repo.users)
        logger.info(
            f'New user created: {message.from_user.first_name} - User ID: {user.id}, Active: {user.active},'
            f' Language: {user.language}'
        )
