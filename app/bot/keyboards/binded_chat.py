from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


class BindedChatCallbackFactory(CallbackData, prefix="binded_chat"):
    user_id: int
    chat_id: int
    message_id: int


def inline_kb_resend_photo_to_binded_chat(user_id: int, chat_id: int, message_id: int):
    return InlineKeyboardButton(
        text='✅',
        callback_data=BindedChatCallbackFactory(
            user_id=user_id,
            chat_id=chat_id,
            message_id=message_id
        ).pack()
    )


def danbooru_post_inline_kb(
        user_id: int,
        message_id: int,
        chat_id: int
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(inline_kb_resend_photo_to_binded_chat(
        user_id=user_id,
        chat_id=chat_id,
        message_id=message_id
    ))
    return builder.as_markup()
