from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Keyboard for selecting a category
categories_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Любые")],
        [KeyboardButton(text="Программистские")],
        [KeyboardButton(text="Разнообразные")],
        [KeyboardButton(text="Черные")],
        [KeyboardButton(text="Каламбурные")],
        [KeyboardButton(text="Жуткие")],
        [KeyboardButton(text="Новогодние")],
        [KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True
)

# Keyboard for selecting the type of joke
types_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Односоставные")],
        [KeyboardButton(text="Двусоставные")],
        [KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True
)

# Keyboard for flags (additional parameters)
flags_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Любые")],
        [KeyboardButton(text="Без NSFW")],
        [KeyboardButton(text="Без религиозных")],
        [KeyboardButton(text="Без политических")],
        [KeyboardButton(text="Без расистских")],
        [KeyboardButton(text="Без сексистских")],
        [KeyboardButton(text="safe-mode")],
        [KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True
)
