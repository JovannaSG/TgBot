import asyncio
import logging
from aiogram import Router, types
from aiogram.filters import Command


router = Router()


@router.message(Command("user_info"))
async def user_info(message: types.Message):
    await message.reply(
        "Информация о вас:" +
        "\nID: " + str(message.from_user.id) +
        "\nfirst_name: " + str(message.from_user.first_name) + 
        "\nlast_name: " + str(message.from_user.last_name) +
        "\nusername: " + str(message.from_user.username)
    )
