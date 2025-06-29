from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

buttons = [
    [
        types.InlineKeyboardButton(
            text="Вернуться назад",
            callback_data="close_weather_foreacast"
        )
    ]
]
keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
