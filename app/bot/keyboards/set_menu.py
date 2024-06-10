from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot) -> bool:
    main_menu_commands = [
        BotCommand(command='/adminlist',
                   description='Список админов')
    ]

    return await bot.set_my_commands(main_menu_commands)

