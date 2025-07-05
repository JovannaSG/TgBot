from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup
)

# Create buttons for main menu
button_get_weather_forecast = KeyboardButton(text="Получить прогноз погоды🌤️")
button_get_joke = KeyboardButton(text="Получить шутку🤡")

# Create keyboard
main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [button_get_weather_forecast, button_get_joke]
    ],
    resize_keyboard=True
)
