from aiogram import Router

from . import external_api
from . import admin, basic, errors


def setup():
    router = Router()
    router.include_routers(
        external_api.setup(),
        admin.router,
        basic.router,
        errors.router
    )
    return router
