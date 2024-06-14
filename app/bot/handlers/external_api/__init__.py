from aiogram import Router

from . import danbooru


def setup():
    router = Router()
    router.include_routers(
        danbooru.router
    )
    return router
