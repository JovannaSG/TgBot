from aiogram import Router, types
from aiogram.filters import Command

from main import bot

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
    await message.answer("Выберите действие")


@router.message(Command("user_info", prefix="/"))
async def user_info(message: types.Message):
    await message.reply(
        "Информация о вас:" +
        "\nID: " + str(message.from_user.id) +
        "\nfirst_name: " + str(message.from_user.first_name) + 
        "\nlast_name: " + str(message.from_user.last_name) +
        "\nusername: " + str(message.from_user.username)
    )
