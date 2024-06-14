from aiogram import Router

from .danbooru import danbooru_router


def setup():
    router = Router()
    router.include_routers(
        danbooru_router
    )
    return router
