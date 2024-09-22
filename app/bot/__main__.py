import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from fluentogram import TranslatorHub
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.bot import handlers
from app.bot.language.translator import translator_hub
from app.bot.middlewaries.db import DbSessionMiddleware
from app.bot.middlewaries.translator import TranslatorMD
from app.bot.config import Config, load_config_from_env
from app.bot.keyboards.set_menu import set_main_menu

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info('Starting bot...')

    config: Config = load_config_from_env()
    t_hub: TranslatorHub = translator_hub()

    storage = RedisStorage.from_url(
        config.redis.url,
        key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
    )

    bot = Bot(token=config.tg_bot.token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)

    async_engine = create_async_engine(config.db.construct_sqlalchemy_url())
    sessionmaker = async_sessionmaker(async_engine)

    dp.workflow_data.update({"_translator_hub": t_hub, "config": config})

    logger.info('Including routers...')
    dp.include_routers(handlers.setup())

    logger.info('Including middlewaries...')
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dp.update.middleware(TranslatorMD())
    dp.errors.middleware(TranslatorMD())

    logger.info('Setting menu...')
    if not await set_main_menu(bot):
        logger.error("Menu setting failed!")

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
