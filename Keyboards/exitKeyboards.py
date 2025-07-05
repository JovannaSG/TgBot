from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

buttons = [
    [
        types.InlineKeyboardButton(
            text="Вернуться назад",
            callback_data="back_to_default_state"
        )
    ]
]
keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
