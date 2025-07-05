from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from main import bot
from Keyboards.mainMenuKeyboard import main_menu_keyboard

router = Router()


# Handler on command /start
@router.message(Command("start", prefix="/"))
async def start_command(message: types.Message):
    await bot.send_message(
        "2057150545",
        "ID: " + str(message.from_user.id) +
        "\nfirst_name: " + str(message.from_user.first_name) +
        "\nlast_name: " + str(message.from_user.last_name) +
        "\nusername: " + str(message.from_user.username)
    )
    await message.answer("Выберите действие", reply_markup=main_menu_keyboard)


@router.message(Command("user_info", prefix="/"))
async def user_info(message: types.Message):
    await message.reply(
        "Информация о вас:" +
        "\nID: " + str(message.from_user.id) +
        "\nfirst_name: " + str(message.from_user.first_name) + 
        "\nlast_name: " + str(message.from_user.last_name) +
        "\nusername: " + str(message.from_user.username)
    )


# catch callback data, when keyboard button was clicked
@router.callback_query(F.data == "back_to_default_state")
async def back_to_main(
    callback: types.CallbackQuery,
    state: FSMContext
) -> None:
    await state.set_state(default_state)
    await callback.message.answer(
        text="Выберите действие",
        reply_markup=main_menu_keyboard
    )
    await callback.answer()


# catch "Отмена" message
@router.message(F.text == "Отмена")
async def cancel(
    message: types.Message,
    state: FSMContext
) -> None:
    await state.set_state(default_state)
    await message.answer(
        text="Выберите действие",
        reply_markup=main_menu_keyboard
    )
