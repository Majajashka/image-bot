from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot) -> bool:
    main_menu_commands = [
        BotCommand(command='/danbooru',
                   description='<count> <tags>'),
        BotCommand(command='/search',
                   description='Search tags'),
        BotCommand(command='/default_tags',
                   description='Set tags that will be applied to every post request'),
        BotCommand(command='/default_count',
                   description='Set count of posts that will be applied to every post request')
    ]

    return await bot.set_my_commands(main_menu_commands)
