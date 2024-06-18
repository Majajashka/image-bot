import logging

from aiogram import Router
from aiogram.filters.exception import ExceptionTypeFilter, ErrorEvent
from fluentogram import TranslatorRunner

from app.core.utils.expections import (
    UserArgumentError,
    ApiError,
    InvalidRequestCount,
    InvalidTagsCount,
    DanbooruApiError
)

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.errors(ExceptionTypeFilter(UserArgumentError))
async def invalid_input(error: ErrorEvent, i18n: TranslatorRunner):
    exception = error.exception
    message = error.update.message

    if isinstance(exception, InvalidRequestCount):
        await message.answer(i18n.error.request_args.post_count(max_posts=exception.max_count))
    if isinstance(exception, InvalidTagsCount):
        await message.answer(i18n.error.request_args.tags_count(max_tags=exception.count))
    logger.debug(repr(exception))


@router.errors(ExceptionTypeFilter(ApiError))
async def api_error(error: ErrorEvent, i18n: TranslatorRunner):
    exception = error.exception
    message = error.update.message

    if isinstance(exception, DanbooruApiError):
        await message.answer(text=i18n.error.api(response_status=exception.response_status, **exception.__dict__))

    elif isinstance(exception, ApiError):
        await message.answer(text=i18n.error.api(response_status=exception.response_status, **exception.__dict__))

    logger.exception(
        f"Cause {exception.__class__.__name__}:\n"
        f"{await exception.response_json_dump}",
        exc_info=exception
    )


@router.errors()
async def undefined_error(error: ErrorEvent):
    logger.exception(
        "Cause unexpected exception %s, by processing %s",
        error.exception.__class__.__name__,
        error.update.model_dump(exclude_none=True),
        exc_info=error.exception,
    )
