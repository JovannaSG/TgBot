import aiohttp

from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup

from Keyboards.jokeRouterKeyboard import (
    categories_keyboard,
    types_keyboard,
    flags_keyboard
)
from Keyboards.mainMenuKeyboard import main_menu_keyboard
from Keyboards.exitKeyboards import keyboard

router = Router()


class JokeStates(StatesGroup):
    waiting_for_category = State()
    waiting_for_type = State()
    waiting_for_flags = State()


@router.message(F.text == "Получить шутку🤡", StateFilter(default_state))
async def start_route_joke(message: types.Message, state: FSMContext):
    await message.answer(
        "Выбери категорию шутки:",
        reply_markup=categories_keyboard
    )
    await state.set_state(JokeStates.waiting_for_category)


# Category selection handler
@router.message(StateFilter(JokeStates.waiting_for_category))
async def process_category(message: types.Message, state: FSMContext):
    category_map: dict = {
        "Любые": "Any",
        "Программистские": "Programming",
        "Разнообраные": "Misc",  # Miscellaneous
        "Черные": "Dark",
        "Каламбурные": "Pun",
        "Жуткие": "Spooky",
        "Новогодние": "Christmas"
    }

    if message.text not in category_map:
        await message.answer("Пожалуйста, выбери категорию из предложенных.")
        return

    await state.update_data(category=category_map[message.text])
    await state.set_state(JokeStates.waiting_for_type)
    await message.answer(
        "Выбери тип шутки:",
        reply_markup=types_keyboard
    )


# Handler for selecting the type of joke
@router.message(StateFilter(JokeStates.waiting_for_type))
async def process_type(message: types.Message, state: FSMContext):
    type_map: dict = {
        "Односоставные": "single",
        "Двусоставные": "twopart"
    }

    if message.text not in type_map:
        await message.answer("Пожалуйста, выбери тип из предложенных.")
        return

    await state.update_data(type=type_map[message.text])
    await state.set_state(JokeStates.waiting_for_flags)
    await message.answer(
        "Выбери ограничения для шутки:",
        reply_markup=flags_keyboard
    )


# Flag selection handler
@router.message(StateFilter(JokeStates.waiting_for_flags))
async def process_flags(message: types.Message, state: FSMContext):
    flags_map = {
        "Любые": "",
        "Без NSFW": "nsfw",
        "Без религиозных": "religious",
        "Без политических": "political",
        "Без расистских": "racist",
        "Без сексистских": "sexist",
        "safe_mode": "safe-mode"
    }

    if message.text not in flags_map:
        await message.answer("Пожалуйста, выбери ограничения из предложенных.")
        return

    data = await state.get_data()
    await state.clear()

    # Creating the URL for the JokeAPI request
    url: str = "https://v2.jokeapi.dev/joke/"
    url += data["category"] + "?"

    if data["type"] != "any":
        url += "type={}&".format(data["type"])

    if message.text != "Любые":
        if flags_map[message.text] == "safe-mode":
            url += "safe-mode&"
        else:
            url += f"blacklistFlags={flags_map[message.text]}&"

    # Delete the last character (&), if there is one
    url = url.rstrip("&")

    # Getting a joke
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    joke_data = await response.json()

                    if joke_data["type"] == "single":
                        joke_text = joke_data["joke"]
                    else:
                        joke_text = "{}\n\n{}".format(
                            joke_data["setup"],
                            joke_data["delivery"]
                        )
                    await message.answer(
                        joke_text,
                        reply_markup=main_menu_keyboard
                    )
                else:
                    await message.answer(
                        "Не удалось получить шутку. Попробуй ещё раз позже.",
                        reply_markup=main_menu_keyboard
                    )
        except Exception as e:
            await message.answer(
                "Произошла ошибка при получении шутки. Попробуй ещё раз.",
                reply_markup=main_menu_keyboard
            )
