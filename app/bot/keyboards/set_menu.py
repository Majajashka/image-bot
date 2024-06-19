from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot) -> bool:
    main_menu_commands = [
        BotCommand(command='/danbooru',
                   description='<count> <tags>'),
        BotCommand(command='/search',
                   description='Search tags')
    ]

    return await bot.set_my_commands(main_menu_commands)
